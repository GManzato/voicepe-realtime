"""The router backend is told who is speaking (app/speaker_context.py)."""
import time
import unittest

from app.speaker_context import SpeakerProbe, router_note


def probe_with(label, name, method):
    probe = SpeakerProbe("Alex", "Sam")
    probe.current_label, probe.current_name, probe.current_method = label, name, method
    probe._verdict_at = time.monotonic()
    return probe


class RouterNote(unittest.TestCase):
    def test_a_voiceprint_match_names_the_speaker(self):
        note = router_note(probe_with("male", "Alex", "voiceprint"))
        self.assertIn("Alex", note)
        self.assertIn("voice print", note)

    def test_a_pitch_guess_names_the_speaker_with_a_caveat(self):
        note = router_note(probe_with("female", "Sam", "pitch(vp=uncertain:0.34)"))
        self.assertIn("Sam", note)
        self.assertIn("may be wrong", note)

    def test_a_stale_verdict_names_nobody(self):
        probe = probe_with("male", "Alex", "voiceprint")
        probe._verdict_at = time.monotonic() - 3600
        self.assertNotIn("Alex", router_note(probe))

    def test_a_guest_and_an_unidentified_speaker(self):
        self.assertIn("did not match", router_note(probe_with("unknown", None, "voiceprint")))
        self.assertIn("not identified", router_note(probe_with("uncertain", None, "pitch")))

    def test_no_probe_or_no_names_adds_nothing(self):
        self.assertEqual(router_note(None), "")
        self.assertEqual(router_note(SpeakerProbe("", "")), "")


if __name__ == "__main__":
    unittest.main()
