"""Kiểm thử dựa trên tính chất + đối chiếu ngẫu nhiên với reference_sim (TV5 - Duy)."""
import random
import unittest

from helpers import ALGOS, run, by_pid, as_tuple, check_invariants
from reference_sim import simulate


def random_rows(rng, max_n=30, max_at=40, max_bt=15):
    n = rng.randint(1, max_n)
    ids = [f"P{i}" for i in range(n)]
    rng.shuffle(ids)
    return [(pid, rng.randint(0, max_at), rng.randint(1, max_bt)) for pid in ids]


class TestRandomDifferential(unittest.TestCase):
    def test_engine_matches_reference_on_random_inputs(self):
        for algo in ALGOS:
            for seed in range(300):
                rows = random_rows(random.Random(seed))
                with self.subTest(algo=algo, seed=seed):
                    results, gantt = run(algo, rows)
                    ref, ref_gantt = simulate(rows, algo)
                    self.assertEqual({k: as_tuple(v) for k, v in by_pid(results).items()}, ref)
                    self.assertEqual(gantt, ref_gantt)
                    check_invariants(self, rows, results, gantt)

    def test_dense_ties(self):
        """AT và BT lấy trong khoảng rất hẹp -> hầu như mọi quyết định đều là tie-break."""
        for algo in ALGOS:
            for seed in range(200):
                rng = random.Random(1000 + seed)
                n = rng.randint(2, 12)
                rows = [(f"P{i}", rng.randint(0, 2), rng.randint(1, 3)) for i in range(n)]
                with self.subTest(algo=algo, seed=seed):
                    results, gantt = run(algo, rows)
                    ref, ref_gantt = simulate(rows, algo)
                    self.assertEqual({k: as_tuple(v) for k, v in by_pid(results).items()}, ref)
                    self.assertEqual(gantt, ref_gantt)

    def test_sparse_arrivals_many_idle(self):
        for algo in ALGOS:
            for seed in range(100):
                rng = random.Random(5000 + seed)
                rows = [(f"P{i}", rng.randint(0, 500), rng.randint(1, 5)) for i in range(rng.randint(1, 15))]
                with self.subTest(algo=algo, seed=seed):
                    results, gantt = run(algo, rows)
                    self.assertEqual(gantt, simulate(rows, algo)[1])


if __name__ == "__main__":
    unittest.main()
