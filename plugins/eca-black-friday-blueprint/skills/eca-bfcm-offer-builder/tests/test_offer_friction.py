import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'offer_friction.py'


class OfferInputTests(unittest.TestCase):
    def run_offer(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              capture_output=True, text=True, encoding='utf-8',
                              env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'})

    def test_blank_offer_is_invalid(self):
        for line in ['', '   ', '\t\n']:
            with self.subTest(line=line):
                result = self.run_offer('--line', line)
                self.assertEqual(result.returncode, 2)
                self.assertIn('--line must contain a non-empty offer', result.stderr)
                self.assertNotIn('CLEAN', result.stdout)

    def test_nonpositive_tiers_are_invalid(self):
        for tiers in ['0', '-2']:
            with self.subTest(tiers=tiers):
                result = self.run_offer('--line', '30% off everything', '--tiers', tiers)
                self.assertEqual(result.returncode, 2)
                self.assertIn('--tiers must be at least 1', result.stderr)

    def test_valid_threshold_offer_retains_success(self):
        result = self.run_offer('--line', 'Spend $100, save $25', '--threshold')
        self.assertEqual(result.returncode, 0)
        self.assertIn('Friction: 1', result.stdout)

    def test_complex_offer_retains_rework_exit(self):
        result = self.run_offer('--line', '30% off everything', '--tiers', '5')
        self.assertEqual(result.returncode, 1)
        self.assertIn('TOO COMPLICATED', result.stdout)


if __name__ == '__main__':
    unittest.main()
