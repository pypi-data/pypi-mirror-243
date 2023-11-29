from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from miditoolkit import (
    Instrument,
    MidiFile,
    Note,
    Pedal,
    PitchBend,
    TempoChange,
    TimeSignature,
)

from ..classes import Event, TokSequence
from ..constants import (
    MIDI_INSTRUMENTS,
    TIME_DIVISION,
    TIME_SIGNATURE,
)
from ..midi_tokenizer import MIDITokenizer, _in_as_seq
from ..utils import fix_offsets_overlapping_notes, set_midi_max_tick


class MIDILike(MIDITokenizer):
    r"""Introduced in `This time with feeling (Oore et al.) <https://arxiv.org/abs/1808.03715>`_
    and later used with `Music Transformer (Huang et al.) <https://openreview.net/forum?id=rJe4ShAcF7>`_
    and `MT3 (Gardner et al.) <https://openreview.net/forum?id=iMSjopcOn0p>`_,
    this tokenization simply converts MIDI messages (*NoteOn*, *NoteOff*, *TimeShift*...)
    as tokens, hence the name "MIDI-Like".
    If you specify `use_programs` as `True` in the config file, the tokenizer will add `Program` tokens before
    each `Pitch` tokens to specify its instrument, and will treat all tracks as a single stream of tokens.

    **Note:** as `MIDILike` uses *TimeShifts* events to move the time from note to
    note, it could be unsuited for tracks with long pauses. In such case, the
    maximum *TimeShift* value will be used. Also, the `MIDILike` tokenizer might alter the durations of overlapping
    notes. If two notes of the same instrument with the same pitch are overlapping, i.e. a first one is still being
    played when a second one is also played, the offset time of the first will be set to the onset time of the second.
    This is done to prevent unwanted duration alterations that could happen in such case, as the `NoteOff` token
    associated to the first note will also end the second one.
    **Note:** When decoding multiple token sequences (of multiple tracks), i.e. when `config.use_programs` is False,
    only the tempos and time signatures of the first sequence will be decoded for the whole MIDI.
    """

    def _tweak_config_before_creating_voc(self):
        self._note_on_off = True

    def _add_time_events(self, events: List[Event]) -> List[Event]:
        r"""
        Takes a sequence of note events (containing optionally Chord, Tempo and TimeSignature tokens),
        and insert (not inplace) time tokens (TimeShift, Rest) to complete the sequence.

        :param events: note events to complete.
        :return: the same events, with time events inserted.
        """

        # Add time events
        all_events = []
        previous_tick = 0
        previous_note_end = 0
        for e, event in enumerate(events):
            # No time shift
            if event.time != previous_tick:
                # (Rest)
                if (
                    self.config.use_rests
                    and event.time - previous_note_end >= self._min_rest
                ):
                    previous_tick = previous_note_end
                    rest_values = self._ticks_to_duration_tokens(
                        event.time - previous_tick, rest=True
                    )
                    for dur_value, dur_ticks in zip(*rest_values):
                        all_events.append(
                            Event(
                                type="Rest",
                                value=".".join(map(str, dur_value)),
                                time=previous_tick,
                                desc=f"{event.time - previous_tick} ticks",
                            )
                        )
                        previous_tick += dur_ticks

                # Time shift
                # no else here as previous might have changed with rests
                if event.time != previous_tick:
                    time_shift = event.time - previous_tick
                    for dur_value, dur_ticks in zip(
                        *self._ticks_to_duration_tokens(time_shift)
                    ):
                        all_events.append(
                            Event(
                                type="TimeShift",
                                value=".".join(map(str, dur_value)),
                                time=previous_tick,
                                desc=f"{time_shift} ticks",
                            )
                        )
                        previous_tick += dur_ticks
                previous_tick = event.time

            all_events.append(event)

            # Update max offset time of the notes encountered
            if event.type in ["NoteOn", "PitchIntervalTime", "PitchIntervalChord"]:
                previous_note_end = max(previous_note_end, event.desc)
            elif event.type in [
                "Program",
                "Tempo",
                "Pedal",
                "PedalOff",
                "PitchBend",
                "Chord",
            ]:
                previous_note_end = max(previous_note_end, event.time)

        return all_events

    def _midi_to_tokens(
        self, midi: MidiFile, *args, **kwargs
    ) -> Union[TokSequence, List[TokSequence]]:
        r"""Converts a preprocessed MIDI object to a sequence of tokens.
        Overridden to call fix_offsets_overlapping_notes before.

        :param midi: the MIDI object to convert.
        :return: a :class:`miditok.TokSequence` if `tokenizer.one_token_stream` is true, else a list of
                :class:`miditok.TokSequence` objects.
        """
        # Adds note tokens
        for track in midi.instruments:
            # Fix offsets overlapping notes
            fix_offsets_overlapping_notes(track.notes)

        return super()._midi_to_tokens(midi, *args, **kwargs)

    @_in_as_seq()
    def tokens_to_midi(
        self,
        tokens: Union[
            Union[TokSequence, List, np.ndarray, Any],
            List[Union[TokSequence, List, np.ndarray, Any]],
        ],
        programs: Optional[List[Tuple[int, bool]]] = None,
        output_path: Optional[str] = None,
        time_division: int = TIME_DIVISION,
        default_duration: int = None,
    ) -> MidiFile:
        r"""Converts tokens (:class:`miditok.TokSequence`) into a MIDI and saves it.

        :param tokens: tokens to convert. Can be either a list of :class:`miditok.TokSequence`,
        :param programs: programs of the tracks. If none is given, will default to piano, program 0. (default: None)
        :param output_path: path to save the file. (default: None)
        :param time_division: MIDI time division / resolution, in ticks/beat (of the MIDI to create).
        :param default_duration: default duration (in ticks) in case a Note On event occurs without its associated
                note off event. Leave None to discard Note On with no Note Off event.
        :return: the midi object (:class:`miditoolkit.MidiFile`).
        """
        # Unsqueeze tokens in case of one_token_stream
        if self.one_token_stream:  # ie single token seq
            tokens = [tokens]
        for i in range(len(tokens)):
            tokens[i] = tokens[i].tokens
        midi = MidiFile(ticks_per_beat=time_division)
        assert (
            time_division % max(self.config.beat_res.values()) == 0
        ), f"Invalid time division, please give one divisible by {max(self.config.beat_res.values())}"
        if time_division in self._durations_ticks:
            max_duration_tok_tick = max(self._durations_ticks[time_division])
        else:
            max_duration_tok_tick = self._token_duration_to_ticks(
                self.durations[-1], time_division
            )

        # RESULTS
        instruments: Dict[int, Instrument] = {}
        tempo_changes = [TempoChange(self._DEFAULT_TEMPO, -1)]
        time_signature_changes = [TimeSignature(*TIME_SIGNATURE, 0)]
        active_notes = {p: {} for p in self.config.programs}

        def check_inst(prog: int):
            if prog not in instruments.keys():
                instruments[prog] = Instrument(
                    program=0 if prog == -1 else prog,
                    is_drum=prog == -1,
                    name="Drums" if prog == -1 else MIDI_INSTRUMENTS[prog]["name"],
                )

        def clear_active_notes():
            if default_duration is not None:
                if self.one_token_stream:
                    for program, active_notes_ in active_notes.items():
                        for pitch_, (onset_tick, vel_) in active_notes_.items():
                            check_inst(program)
                            instruments[program].notes.append(
                                Note(
                                    vel_,
                                    pitch_,
                                    onset_tick,
                                    onset_tick + default_duration,
                                )
                            )
                else:
                    for pitch_, (onset_tick, vel_) in active_notes[
                        current_instrument.program
                    ].items():
                        current_instrument.notes.append(
                            Note(
                                vel_, pitch_, onset_tick, onset_tick + default_duration
                            )
                        )

        current_instrument = None
        for si, seq in enumerate(tokens):
            # Set tracking variables
            current_tick = 0
            current_program = 0
            previous_pitch_onset = {prog: -128 for prog in self.config.programs}
            previous_pitch_chord = {prog: -128 for prog in self.config.programs}
            active_pedals = {}
            # Set track / sequence program if needed
            if not self.one_token_stream:
                is_drum = False
                if programs is not None:
                    current_program, is_drum = programs[si]
                current_instrument = Instrument(
                    program=current_program,
                    is_drum=is_drum,
                    name="Drums"
                    if current_program == -1
                    else MIDI_INSTRUMENTS[current_program]["name"],
                )

            # Decode tokens
            for ti, token in enumerate(seq):
                tok_type, tok_val = token.split("_")
                if tok_type in ["TimeShift", "Rest"]:
                    current_tick += self._token_duration_to_ticks(
                        tok_val, time_division
                    )
                elif tok_type in [
                    "NoteOn",
                    "NoteOff",
                    "PitchIntervalTime",
                    "PitchIntervalChord",
                ]:
                    # We update previous_pitch_onset and previous_pitch_chord even if the try fails.
                    if tok_type == "PitchIntervalTime":
                        pitch = previous_pitch_onset[current_program] + int(tok_val)
                        previous_pitch_onset[current_program] = pitch
                        previous_pitch_chord[current_program] = pitch
                    elif tok_type == "PitchIntervalChord":
                        pitch = previous_pitch_chord[current_program] + int(tok_val)
                        previous_pitch_chord[current_program] = pitch
                    else:
                        pitch = int(tok_val)
                        if tok_type == "NoteOn":
                            previous_pitch_onset[current_program] = pitch
                            previous_pitch_chord[current_program] = pitch
                    # if NoteOn and already active, end the active note here, but this shouldn't happen
                    if pitch in active_notes[current_program]:
                        note_onset_tick, vel = active_notes[current_program][pitch]
                        offset_tick = current_tick
                        if current_tick - note_onset_tick > max_duration_tok_tick:
                            if default_duration is not None:
                                offset_tick = note_onset_tick + default_duration
                            else:
                                continue
                        new_note = Note(vel, pitch, note_onset_tick, offset_tick)
                        if self.one_token_stream:
                            check_inst(current_program)
                            instruments[current_program].notes.append(new_note)
                        else:
                            current_instrument.notes.append(new_note)
                        del active_notes[current_program][pitch]
                    if tok_type != "NoteOff" and ti + 1 < len(seq):
                        vel = int(seq[ti + 1].split("_")[1])
                        active_notes[current_program][pitch] = (current_tick, vel)
                elif tok_type == "Program":
                    current_program = int(tok_val)
                elif tok_type == "Tempo":
                    # If your encoding include tempo tokens, each Position token should be followed by
                    # a tempo token, but if it is not the case this method will skip this step
                    tempo = float(tok_val)
                    if si == 0 and current_tick != tempo_changes[-1].time:
                        tempo_changes.append(TempoChange(tempo, current_tick))
                elif si == 0 and tok_type == "TimeSig":
                    num, den = self._parse_token_time_signature(tok_val)
                    current_time_signature = time_signature_changes[-1]
                    if (
                        num != current_time_signature.numerator
                        or den != current_time_signature.denominator
                    ):
                        time_signature_changes.append(
                            TimeSignature(num, den, current_tick)
                        )
                elif tok_type == "Pedal":
                    pedal_prog = (
                        int(tok_val) if self.config.use_programs else current_program
                    )
                    if self.config.sustain_pedal_duration and ti + 1 < len(seq):
                        if seq[ti + 1].split("_")[0] == "Duration":
                            duration = self._token_duration_to_ticks(
                                seq[ti + 1].split("_")[1], time_division
                            )
                            # Add instrument if it doesn't exist, can happen for the first tokens
                            new_pedal = Pedal(current_tick, current_tick + duration)
                            if self.one_token_stream:
                                check_inst(pedal_prog)
                                instruments[pedal_prog].pedals.append(new_pedal)
                            else:
                                current_instrument.pedals.append(new_pedal)
                    else:
                        if pedal_prog not in active_pedals:
                            active_pedals[pedal_prog] = current_tick
                elif tok_type == "PedalOff":
                    pedal_prog = (
                        int(tok_val) if self.config.use_programs else current_program
                    )
                    if pedal_prog in active_pedals:
                        new_pedal = Pedal(active_pedals[pedal_prog], current_tick)
                        if self.one_token_stream:
                            check_inst(pedal_prog)
                            instruments[pedal_prog].pedals.append(
                                Pedal(active_pedals[pedal_prog], current_tick)
                            )
                        else:
                            current_instrument.pedals.append(new_pedal)
                        del active_pedals[pedal_prog]
                elif tok_type == "PitchBend":
                    new_pitch_bend = PitchBend(int(tok_val), current_tick)
                    if self.one_token_stream:
                        check_inst(current_program)
                        instruments[current_program].pitch_bends.append(new_pitch_bend)
                    else:
                        current_instrument.pitch_bends.append(new_pitch_bend)

            # Add current_inst to midi and handle notes still active
            if not self.one_token_stream:
                midi.instruments.append(current_instrument)
                clear_active_notes()
                active_notes[current_instrument.program] = {}

        # Handle notes still active
        if self.one_token_stream:
            clear_active_notes()
        if len(tempo_changes) > 1:
            del tempo_changes[0]  # delete mocked tempo change
        tempo_changes[0].time = 0
        if len(time_signature_changes) > 1:
            del time_signature_changes[0]  # delete mocked time signature change
        time_signature_changes[0].time = 0

        # create MidiFile
        if self.one_token_stream:
            midi.instruments = list(instruments.values())
        midi.tempo_changes = tempo_changes
        midi.time_signature_changes = time_signature_changes
        set_midi_max_tick(midi)
        # Write MIDI file
        if output_path:
            Path(output_path).mkdir(parents=True, exist_ok=True)
            midi.dump(output_path)
        return midi

    def _create_base_vocabulary(self) -> List[str]:
        r"""Creates the vocabulary, as a list of string tokens.
        Each token as to be given as the form of "Type_Value", separated with an underscore.
        Example: Pitch_58
        The :class:`miditok.MIDITokenizer` main class will then create the "real" vocabulary as
        a dictionary.
        Special tokens have to be given when creating the tokenizer, and
        will be added to the vocabulary by :class:`miditok.MIDITokenizer`.

        :return: the vocabulary as a list of string.
        """
        vocab = []

        # NOTE ON
        vocab += [f"NoteOn_{i}" for i in range(*self.config.pitch_range)]

        # NOTE OFF
        vocab += [f"NoteOff_{i}" for i in range(*self.config.pitch_range)]

        # VELOCITY
        vocab += [f"Velocity_{i}" for i in self.velocities]

        # TIME SHIFTS
        vocab += [
            f'TimeShift_{".".join(map(str, duration))}' for duration in self.durations
        ]

        # Add additional tokens
        self._add_additional_tokens_to_vocab_list(vocab)

        # Add durations if needed
        if self.config.use_sustain_pedals and self.config.sustain_pedal_duration:
            vocab += [
                f'Duration_{".".join(map(str, duration))}'
                for duration in self.durations
            ]

        return vocab

    def _create_token_types_graph(self) -> Dict[str, List[str]]:
        r"""Returns a graph (as a dictionary) of the possible token
        types successions.
        NOTE: Program type is not referenced here, you can add it manually by
        modifying the tokens_types_graph class attribute following your strategy.

        :return: the token types transitions dictionary
        """
        dic = dict()
        dic["NoteOn"] = ["Velocity"]

        if self.config.use_programs:
            first_note_token_type = (
                "NoteOn" if self.config.program_changes else "Program"
            )
            dic["Program"] = ["NoteOn", "NoteOff"]
        else:
            first_note_token_type = "NoteOn"
        dic["Velocity"] = [first_note_token_type, "TimeShift"]
        dic["NoteOff"] = ["NoteOff", first_note_token_type, "TimeShift"]
        dic["TimeShift"] = ["NoteOff", first_note_token_type, "TimeShift"]
        if self.config.use_pitch_intervals:
            for token_type in ("PitchIntervalTime", "PitchIntervalChord"):
                dic[token_type] = ["Velocity"]
                if self.config.use_programs:
                    dic["Program"].append(token_type)
                else:
                    dic["Velocity"].append(token_type)
                    dic["NoteOff"].append(token_type)
                    dic["TimeShift"].append(token_type)
        if self.config.program_changes:
            for token_type in ["Velocity", "NoteOff"]:
                dic[token_type].append("Program")

        if self.config.use_chords:
            dic["Chord"] = [first_note_token_type]
            dic["TimeShift"] += ["Chord"]
            dic["NoteOff"] += ["Chord"]
            if self.config.use_programs:
                dic["Program"].append("Chord")
            if self.config.use_pitch_intervals:
                dic["Chord"] += ["PitchIntervalTime", "PitchIntervalChord"]

        if self.config.use_tempos:
            dic["TimeShift"] += ["Tempo"]
            dic["Tempo"] = [first_note_token_type, "TimeShift"]
            if not self.config.use_programs or self.config.program_changes:
                dic["Tempo"].append("NoteOff")
            if self.config.use_chords:
                dic["Tempo"] += ["Chord"]
            if self.config.use_rests:
                dic["Tempo"].append("Rest")  # only for first token
            if self.config.use_pitch_intervals:
                dic["Tempo"] += ["PitchIntervalTime", "PitchIntervalChord"]

        if self.config.use_time_signatures:
            dic["TimeShift"] += ["TimeSig"]
            dic["TimeSig"] = [first_note_token_type, "TimeShift"]
            if not self.config.use_programs or self.config.program_changes:
                dic["TimeSig"].append("NoteOff")
            if self.config.use_chords:
                dic["TimeSig"] += ["Chord"]
            if self.config.use_rests:
                dic["TimeSig"].append("Rest")  # only for first token
            if self.config.use_tempos:
                dic["TimeSig"].append("Tempo")
            if self.config.use_pitch_intervals:
                dic["TimeSig"] += ["PitchIntervalTime", "PitchIntervalChord"]

        if self.config.use_sustain_pedals:
            dic["TimeShift"].append("Pedal")
            dic["NoteOff"].append("Pedal")
            if not self.config.sustain_pedal_duration:
                dic["NoteOff"].append("PedalOff")
            if self.config.sustain_pedal_duration:
                dic["Pedal"] = ["Duration"]
                dic["Duration"] = [first_note_token_type, "NoteOff", "TimeShift"]
                if self.config.use_pitch_intervals:
                    dic["Duration"] += ["PitchIntervalTime", "PitchIntervalChord"]
            else:
                dic["PedalOff"] = [
                    "Pedal",
                    "PedalOff",
                    first_note_token_type,
                    "NoteOff",
                    "TimeShift",
                ]
                dic["Pedal"] = ["Pedal", first_note_token_type, "NoteOff", "TimeShift"]
                dic["TimeShift"].append("PedalOff")
            if self.config.use_chords:
                dic["Pedal"].append("Chord")
                if not self.config.sustain_pedal_duration:
                    dic["PedalOff"].append("Chord")
                    dic["Chord"].append("PedalOff")
            if self.config.use_rests:
                dic["Pedal"].append("Rest")
                if not self.config.sustain_pedal_duration:
                    dic["PedalOff"].append("Rest")
            if self.config.use_tempos:
                dic["Tempo"].append("Pedal")
                if not self.config.sustain_pedal_duration:
                    dic["Tempo"].append("PedalOff")
            if self.config.use_time_signatures:
                dic["TimeSig"].append("Pedal")
                if not self.config.sustain_pedal_duration:
                    dic["TimeSig"].append("PedalOff")

        if self.config.use_pitch_bends:
            # As a Program token will precede PitchBend otherwise
            # Else no need to add Program as its already in
            dic["PitchBend"] = [first_note_token_type, "NoteOff", "TimeShift"]
            if self.config.use_programs:
                dic["Program"].append("PitchBend")
            if not self.config.programs or self.config.program_changes:
                dic["TimeShift"].append("PitchBend")
                dic["NoteOff"].append("PitchBend")
                if self.config.use_tempos:
                    dic["Tempo"].append("PitchBend")
                if self.config.use_time_signatures:
                    dic["TimeSig"].append("PitchBend")
                if self.config.use_sustain_pedals:
                    dic["Pedal"].append("PitchBend")
                    if self.config.sustain_pedal_duration:
                        dic["Duration"].append("PitchBend")
                    else:
                        dic["PedalOff"].append("PitchBend")
            if self.config.use_chords:
                dic["PitchBend"].append("Chord")
            if self.config.use_rests:
                dic["PitchBend"].append("Rest")

        if self.config.use_rests:
            dic["Rest"] = ["Rest", first_note_token_type, "TimeShift"]
            dic["NoteOff"] += ["Rest"]
            if self.config.use_chords:
                dic["Rest"] += ["Chord"]
            if self.config.use_tempos:
                dic["Rest"].append("Tempo")
            if self.config.use_time_signatures:
                dic["Rest"].append("TimeSig")
            if self.config.use_sustain_pedals:
                dic["Rest"].append("Pedal")
                if self.config.sustain_pedal_duration:
                    dic["Duration"].append("Rest")
                else:
                    dic["Rest"].append("PedalOff")
                    dic["PedalOff"].append("Rest")
            if self.config.use_pitch_bends:
                dic["Rest"].append("PitchBend")
            if self.config.use_pitch_intervals:
                dic["Rest"] += ["PitchIntervalTime", "PitchIntervalChord"]
        else:
            dic["TimeShift"].append("TimeShift")

        if self.config.program_changes:
            for token_type in [
                "TimeShift",
                "Rest",
                "PitchBend",
                "Pedal",
                "PedalOff",
                "Tempo",
                "TimeSig",
                "Chord",
            ]:
                if token_type in dic:
                    dic["Program"].append(token_type)
                    dic[token_type].append("Program")

        return dic

    @_in_as_seq(complete=False, decode_bpe=False)
    def tokens_errors(
        self, tokens: Union[TokSequence, List, np.ndarray, Any]
    ) -> Union[float, List[float]]:
        r"""Checks if a sequence of tokens is made of good token types
        successions and returns the error ratio (lower is better).
        The Pitch and Position values are also analyzed:
            - a NoteOn token should not be present if the same pitch is already being played
            - a NoteOff token should not be present the note is not being played

        :param tokens: sequence of tokens to check
        :return: the error ratio (lower is better)
        """
        # If list of TokSequence -> recursive
        if isinstance(tokens, list):
            return [self.tokens_errors(tok_seq) for tok_seq in tokens]
        if len(tokens) == 0:
            return 0

        nb_tok_predicted = len(tokens)  # used to norm the score
        if self.has_bpe:
            self.decode_bpe(tokens)
        self.complete_sequence(tokens)

        # Override from here

        err = 0
        current_program = 0
        current_pitches = {p: [] for p in self.config.programs}
        current_pitches_tick = {p: [] for p in self.config.programs}
        max_duration = self.durations[-1][0] * max(self.config.beat_res.values())
        max_duration += self.durations[-1][1] * (
            max(self.config.beat_res.values()) // self.durations[-1][2]
        )
        previous_pitch_onset = {program: -128 for program in self.config.programs}
        previous_pitch_chord = {program: -128 for program in self.config.programs}

        events = (
            tokens.events
            if tokens.events is not None
            else [Event(*tok.split("_")) for tok in tokens.tokens]
        )

        for i in range(1, len(events)):
            # err_tokens = events[i - 4 : i + 4]  # uncomment for debug
            # Good token type
            if events[i].type in self.tokens_types_graph[events[i - 1].type]:
                if events[i].type in [
                    "NoteOn",
                    "PitchIntervalTime",
                    "PitchIntervalChord",
                ]:
                    current_program_noff = current_program
                    if events[i].type == "NoteOn":
                        pitch_val = int(events[i].value)
                        previous_pitch_onset[current_program] = pitch_val
                        previous_pitch_chord[current_program] = pitch_val
                    elif events[i].type == "PitchIntervalTime":
                        pitch_val = previous_pitch_onset[current_program] + int(
                            events[i].value
                        )
                        previous_pitch_onset[current_program] = pitch_val
                        previous_pitch_chord[current_program] = pitch_val
                    else:  # PitchIntervalChord
                        pitch_val = previous_pitch_chord[current_program] + int(
                            events[i].value
                        )
                        previous_pitch_chord[current_program] = pitch_val

                    current_pitches[current_program].append(pitch_val)
                    if pitch_val in current_pitches_tick[current_program]:
                        err += 1  # note already being played at current tick
                        continue

                    current_pitches_tick[current_program].append(pitch_val)
                    # look for an associated note off event to get duration
                    offset_sample = 0
                    for j in range(i + 1, len(events)):
                        if (
                            events[j].type == "NoteOff"
                            and int(events[j].value) == pitch_val
                        ):
                            if (
                                self.config.use_programs
                                and current_program_noff == current_program
                            ):
                                break  # all good
                            else:
                                break  # all good
                        elif events[j].type in ["TimeShift", "Rest"]:
                            offset_sample += self._token_duration_to_ticks(
                                events[j].value, max(self.config.beat_res.values())
                            )
                        elif events[j].type == "Program":
                            current_program_noff = events[j].value

                        # will not look for Note Off beyond
                        if offset_sample > max_duration:
                            err += 1
                            break
                elif events[i].type == "NoteOff":
                    if int(events[i].value) not in current_pitches[current_program]:
                        err += 1  # this pitch wasn't being played
                    else:
                        current_pitches[current_program].remove(int(events[i].value))
                elif events[i].type == "Program" and i + 1 < len(events):
                    current_program = int(events[i].value)
                elif events[i].type in ["TimeShift", "Rest"]:
                    current_pitches_tick = {p: [] for p in self.config.programs}

            # Bad token type
            else:
                err += 1

        return err / nb_tok_predicted
