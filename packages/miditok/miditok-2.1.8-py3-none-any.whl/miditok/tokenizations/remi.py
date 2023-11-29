from math import ceil
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

from ..classes import Event, TokenizerConfig, TokSequence
from ..constants import (
    MIDI_INSTRUMENTS,
    TIME_DIVISION,
    TIME_SIGNATURE,
)
from ..midi_tokenizer import MIDITokenizer, _in_as_seq
from ..utils import set_midi_max_tick


class REMI(MIDITokenizer):
    r"""REMI, standing for Revamped MIDI and introduced with the
    `Pop Music Transformer (Huang and Yang) <https://dl.acm.org/doi/10.1145/3394171.3413671>`_,
    is a tokenization that represents notes as successions of *Pitch*, *Velocity* and *Duration*
    tokens, and time with *Bar* and *Position* tokens. A *Bar* token indicate that a new bar
    is beginning, and *Position* the current position within the current bar. The number of
    positions is determined by the ``beat_res`` argument, the maximum value will be used as
    resolution.
    With the `Program` and `TimeSignature` additional tokens enables, this class is equivalent to REMI+.
    REMI+ is an extended version of :ref:`REMI` (Huang and Yang) for general
    multi-track, multi-signature symbolic music sequences, introduced in
    `FIGARO (Rütte et al.) <https://arxiv.org/abs/2201.10936>`, which handle multiple instruments by
    adding `Program` tokens before the `Pitch` ones.

    **Note:** in the original paper, the tempo information is represented as the succession
    of two token types: a *TempoClass* indicating if the tempo is fast or slow, and a
    *TempoValue* indicating its value. MidiTok only uses one *Tempo* token for its value
    (see :ref:`Additional tokens`).
    **Note:** When decoding multiple token sequences (of multiple tracks), i.e. when `config.use_programs` is False,
    only the tempos and time signatures of the first sequence will be decoded for the whole MIDI.

    :param tokenizer_config: the tokenizer's configuration, as a :class:`miditok.classes.TokenizerConfig` object.
    :param max_bar_embedding: Maximum number of bars ("Bar_0", "Bar_1",...,"Bar_{num_bars-1}").
            If None passed, creates "Bar_None" token only in vocabulary for Bar token.
    :param params: path to a tokenizer config file. This will override other arguments and
            load the tokenizer based on the config file. This is particularly useful if the
            tokenizer learned Byte Pair Encoding. (default: None)
    """

    def __init__(
        self,
        tokenizer_config: TokenizerConfig = None,
        max_bar_embedding: Optional[int] = None,
        params: Union[str, Path] = None,
    ):
        if (
            tokenizer_config is not None
            and "max_bar_embedding" not in tokenizer_config.additional_params
        ):
            # If used, this attribute might increase over tokenizations, if the tokenizer encounter longer MIDIs
            tokenizer_config.additional_params["max_bar_embedding"] = max_bar_embedding
        super().__init__(tokenizer_config, params)

    def _tweak_config_before_creating_voc(self):
        # In case the tokenizer has been created without specifying any config or params file path
        if "max_bar_embedding" not in self.config.additional_params:
            # If used, this attribute might increase over tokenizations, if the tokenizer encounter longer MIDIs
            self.config.additional_params["max_bar_embedding"] = None

    def _add_time_events(self, events: List[Event]) -> List[Event]:
        r"""
        Takes a sequence of note events (containing optionally Chord, Tempo and TimeSignature tokens),
        and insert (not inplace) time tokens (TimeShift, Rest) to complete the sequence.

        :param events: note events to complete.
        :return: the same events, with time events inserted.
        """
        time_division = self._current_midi_metadata["time_division"]
        ticks_per_sample = time_division / max(self.config.beat_res.values())

        # Add time events
        all_events = []
        current_bar = -1
        bar_at_last_ts_change = 0
        previous_tick = -1
        previous_note_end = 0
        tick_at_last_ts_change = tick_at_current_bar = 0
        current_time_sig = TIME_SIGNATURE
        ticks_per_bar = self._compute_ticks_per_bar(
            TimeSignature(*current_time_sig, 0), time_division
        )
        # First look for a TimeSig token, if any is given at tick 0, to update current_time_sig
        if self.config.use_time_signatures:
            for event in events:
                if event.type == "TimeSig":
                    current_time_sig = list(map(int, event.value.split("/")))
                    ticks_per_bar = self._compute_ticks_per_bar(
                        TimeSignature(*current_time_sig, event.time), time_division
                    )
                    break
                elif event.type in [
                    "Pitch",
                    "Velocity",
                    "Duration",
                    "PitchBend",
                    "Pedal",
                ]:
                    break
        # Add the time events
        for e, event in enumerate(events):
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
                    # Add Rest events and increment previous_tick
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
                    # We update current_bar and tick_at_current_bar here without creating Bar tokens
                    real_current_bar = (
                        bar_at_last_ts_change
                        + (previous_tick - tick_at_last_ts_change) // ticks_per_bar
                    )
                    if real_current_bar > current_bar:
                        tick_at_current_bar += (
                            real_current_bar - current_bar
                        ) * ticks_per_bar
                        current_bar = real_current_bar

                # Bar
                nb_new_bars = (
                    bar_at_last_ts_change
                    + (event.time - tick_at_last_ts_change) // ticks_per_bar
                    - current_bar
                )
                if nb_new_bars >= 1:
                    for i in range(nb_new_bars):
                        all_events.append(
                            Event(
                                type="Bar",
                                value=str(current_bar + i + 1)
                                if self.config.additional_params["max_bar_embedding"]
                                is not None
                                else "None",
                                time=(current_bar + i + 1) * ticks_per_bar,
                                desc=0,
                            )
                        )
                        # Add a TimeSignature token, except for the last new Bar token if the current event is a TS
                        if self.config.use_time_signatures and not (
                            event.type == "TimeSig" and i + 1 == nb_new_bars
                        ):
                            all_events.append(
                                Event(
                                    type="TimeSig",
                                    value=f"{current_time_sig[0]}/{current_time_sig[1]}",
                                    time=(current_bar + i + 1) * ticks_per_bar,
                                    desc=0,
                                )
                            )
                    current_bar += nb_new_bars
                    tick_at_current_bar = (
                        tick_at_last_ts_change
                        + (current_bar - bar_at_last_ts_change) * ticks_per_bar
                    )

                # Position
                if event.type != "TimeSig":
                    pos_index = int(
                        (event.time - tick_at_current_bar) / ticks_per_sample
                    )
                    all_events.append(
                        Event(
                            type="Position",
                            value=pos_index,
                            time=event.time,
                            desc=event.time,
                        )
                    )

                previous_tick = event.time

            # Update time signature time variables, after adjusting the time (above)
            if event.type == "TimeSig":
                current_time_sig = list(map(int, event.value.split("/")))
                bar_at_last_ts_change += (
                    event.time - tick_at_last_ts_change
                ) // ticks_per_bar
                tick_at_last_ts_change = event.time
                ticks_per_bar = self._compute_ticks_per_bar(
                    TimeSignature(*current_time_sig, event.time), time_division
                )
                # We decrease the previous tick so that a Position token is enforced for the next event
                previous_tick -= 1

            all_events.append(event)

            # Update max offset time of the notes encountered
            if event.type in ["Pitch", "PitchIntervalTime", "PitchIntervalChord"]:
                previous_note_end = max(previous_note_end, event.desc)
            elif event.type in [
                "Program",
                "Tempo",
                "TimeSig",
                "Pedal",
                "PedalOff",
                "PitchBend",
                "Chord",
            ]:
                previous_note_end = max(previous_note_end, event.time)

        return all_events

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
    ) -> MidiFile:
        r"""Converts tokens (:class:`miditok.TokSequence`) into a MIDI and saves it.

        :param tokens: tokens to convert. Can be either a list of :class:`miditok.TokSequence`,
        :param programs: programs of the tracks. If none is given, will default to piano, program 0. (default: None)
        :param output_path: path to save the file. (default: None)
        :param time_division: MIDI time division / resolution, in ticks/beat (of the MIDI to create).
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
        ticks_per_sample = time_division // max(self.config.beat_res.values())

        # RESULTS
        instruments: Dict[int, Instrument] = {}
        tempo_changes = [TempoChange(self._DEFAULT_TEMPO, -1)]
        time_signature_changes = []

        def check_inst(prog: int):
            if prog not in instruments.keys():
                instruments[prog] = Instrument(
                    program=0 if prog == -1 else prog,
                    is_drum=prog == -1,
                    name="Drums" if prog == -1 else MIDI_INSTRUMENTS[prog]["name"],
                )

        current_instrument = None
        for si, seq in enumerate(tokens):
            # First look for the first time signature if needed
            if si == 0:
                if self.config.use_time_signatures:
                    for token in seq:
                        tok_type, tok_val = token.split("_")
                        if tok_type == "TimeSig":
                            time_signature_changes.append(
                                TimeSignature(*list(map(int, tok_val.split("/"))), 0)
                            )
                            break
                        elif tok_type in [
                            "Pitch",
                            "Velocity",
                            "Duration",
                            "PitchBend",
                            "Pedal",
                        ]:
                            break
                if len(time_signature_changes) == 0:
                    time_signature_changes.append(TimeSignature(*TIME_SIGNATURE, 0))
            current_time_sig = time_signature_changes[-1]
            ticks_per_bar = self._compute_ticks_per_bar(current_time_sig, time_division)

            # Set tracking variables
            current_tick = tick_at_last_ts_change = tick_at_current_bar = 0
            current_bar = -1
            bar_at_last_ts_change = 0
            current_program = 0
            previous_note_end = 0
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
                if tok_type == "Bar":
                    current_bar += 1
                    if current_bar > 0:
                        current_tick = tick_at_current_bar + ticks_per_bar
                    tick_at_current_bar = current_tick
                elif tok_type == "Rest":
                    current_tick = max(previous_note_end, current_tick)
                    current_tick += self._token_duration_to_ticks(
                        tok_val, time_division
                    )
                    real_current_bar = (
                        bar_at_last_ts_change
                        + (current_tick - tick_at_last_ts_change) // ticks_per_bar
                    )
                    if real_current_bar > current_bar:
                        tick_at_current_bar += (
                            real_current_bar - current_bar
                        ) * ticks_per_bar
                        current_bar = real_current_bar
                elif tok_type == "Position":
                    if current_bar == -1:
                        # as this Position token occurs before any Bar token
                        current_bar = 0
                    current_tick = tick_at_current_bar + int(tok_val) * ticks_per_sample
                elif tok_type in ["Pitch", "PitchIntervalTime", "PitchIntervalChord"]:
                    if tok_type == "Pitch":
                        pitch = int(tok_val)
                        previous_pitch_onset[current_program] = pitch
                        previous_pitch_chord[current_program] = pitch
                    # We update previous_pitch_onset and previous_pitch_chord even if the try fails.
                    elif tok_type == "PitchIntervalTime":
                        pitch = previous_pitch_onset[current_program] + int(tok_val)
                        previous_pitch_onset[current_program] = pitch
                        previous_pitch_chord[current_program] = pitch
                    else:  # PitchIntervalChord
                        pitch = previous_pitch_chord[current_program] + int(tok_val)
                        previous_pitch_chord[current_program] = pitch
                    try:
                        vel_type, vel = seq[ti + 1].split("_")
                        dur_type, dur = seq[ti + 2].split("_")
                        if vel_type == "Velocity" and dur_type == "Duration":
                            dur = self._token_duration_to_ticks(dur, time_division)
                            new_note = Note(
                                int(vel), pitch, current_tick, current_tick + dur
                            )
                            if self.one_token_stream:
                                check_inst(current_program)
                                instruments[current_program].notes.append(new_note)
                            else:
                                current_instrument.notes.append(new_note)
                            previous_note_end = max(
                                previous_note_end, current_tick + dur
                            )
                    except IndexError:
                        # A well constituted sequence should not raise an exception
                        # However with generated sequences this can happen, or if the sequence isn't finished
                        pass
                elif tok_type == "Program":
                    current_program = int(tok_val)
                elif tok_type == "Tempo":
                    # If your encoding include tempo tokens, each Position token should be followed by
                    # a tempo token, but if it is not the case this method will skip this step
                    tempo = float(tok_val)
                    if si == 0 and current_tick != tempo_changes[-1].time:
                        tempo_changes.append(TempoChange(tempo, current_tick))
                    previous_note_end = max(previous_note_end, current_tick)
                elif tok_type == "TimeSig":
                    num, den = self._parse_token_time_signature(tok_val)
                    if (
                        num != current_time_sig.numerator
                        or den != current_time_sig.denominator
                    ):
                        current_time_sig = TimeSignature(num, den, current_tick)
                        if si == 0:
                            time_signature_changes.append(current_time_sig)
                        tick_at_last_ts_change = tick_at_current_bar  # == current_tick
                        bar_at_last_ts_change = current_bar
                        ticks_per_bar = self._compute_ticks_per_bar(
                            current_time_sig, time_division
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

        if len(tempo_changes) > 1:
            del tempo_changes[0]  # delete mocked tempo change
        tempo_changes[0].time = 0

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

        # BAR
        if self.config.additional_params["max_bar_embedding"] is not None:
            vocab += [
                f"Bar_{i}"
                for i in range(self.config.additional_params["max_bar_embedding"])
            ]
        else:
            vocab += ["Bar_None"]

        # PITCH
        vocab += [f"Pitch_{i}" for i in range(*self.config.pitch_range)]

        # VELOCITY
        vocab += [f"Velocity_{i}" for i in self.velocities]

        # DURATION
        vocab += [
            f'Duration_{".".join(map(str, duration))}' for duration in self.durations
        ]

        # POSITION
        max_nb_beats = max(
            map(lambda ts: ceil(4 * ts[0] / ts[1]), self.time_signatures)
        )
        nb_positions = max(self.config.beat_res.values()) * max_nb_beats
        vocab += [f"Position_{i}" for i in range(nb_positions)]

        # Add additional tokens
        self._add_additional_tokens_to_vocab_list(vocab)

        return vocab

    def _create_token_types_graph(self) -> Dict[str, List[str]]:
        r"""Returns a graph (as a dictionary) of the possible token
        types successions.

        :return: the token types transitions dictionary
        """
        dic: Dict[str, List[str]] = dict()

        if self.config.use_programs:
            first_note_token_type = (
                "Pitch" if self.config.program_changes else "Program"
            )
            dic["Program"] = ["Pitch"]
        else:
            first_note_token_type = "Pitch"
        dic["Pitch"] = ["Velocity"]
        dic["Velocity"] = ["Duration"]
        dic["Duration"] = [first_note_token_type, "Position", "Bar"]
        dic["Bar"] = ["Position", "Bar"]
        dic["Position"] = [first_note_token_type]
        if self.config.use_pitch_intervals:
            for token_type in ("PitchIntervalTime", "PitchIntervalChord"):
                dic[token_type] = ["Velocity"]
                if self.config.use_programs:
                    dic["Program"].append(token_type)
                else:
                    dic["Duration"].append(token_type)
                    dic["Position"].append(token_type)
        if self.config.program_changes:
            dic["Duration"].append("Program")

        if self.config.use_chords:
            dic["Chord"] = [first_note_token_type]
            dic["Position"] += ["Chord"]
            if self.config.use_programs:
                dic["Program"].append("Chord")
            if self.config.use_pitch_intervals:
                dic["Chord"] += ["PitchIntervalTime", "PitchIntervalChord"]

        if self.config.use_tempos:
            dic["Position"] += ["Tempo"]
            dic["Tempo"] = [first_note_token_type, "Position", "Bar"]
            if self.config.use_chords:
                dic["Tempo"] += ["Chord"]
            if self.config.use_rests:
                dic["Tempo"].append("Rest")  # only for first token
            if self.config.use_pitch_intervals:
                dic["Tempo"] += ["PitchIntervalTime", "PitchIntervalChord"]

        if self.config.use_time_signatures:
            dic["Bar"] = ["TimeSig"]
            dic["TimeSig"] = [first_note_token_type, "Position", "Bar"]
            if self.config.use_chords:
                dic["TimeSig"] += ["Chord"]
            if self.config.use_rests:
                dic["TimeSig"].append("Rest")  # only for first token
            if self.config.use_tempos:
                dic["Tempo"].append("TimeSig")
            if self.config.use_pitch_intervals:
                dic["TimeSig"] += ["PitchIntervalTime", "PitchIntervalChord"]

        if self.config.use_sustain_pedals:
            dic["Position"].append("Pedal")
            if self.config.sustain_pedal_duration:
                dic["Pedal"] = ["Duration"]
            else:
                dic["PedalOff"] = [
                    "Pedal",
                    "PedalOff",
                    first_note_token_type,
                    "Position",
                    "Bar",
                ]
                dic["Pedal"] = ["Pedal", first_note_token_type, "Position", "Bar"]
                dic["Position"].append("PedalOff")
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
            dic["PitchBend"] = [first_note_token_type, "Position", "Bar"]
            if self.config.use_programs:
                dic["Program"].append("PitchBend")
            if not self.config.programs or self.config.program_changes:
                dic["Position"].append("PitchBend")
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
            dic["Rest"] = ["Rest", first_note_token_type, "Position", "Bar"]
            dic["Duration"].append("Rest")
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

        if self.config.program_changes:
            for token_type in [
                "Position",
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
