from fmot.test.utm.get_utms import ALL_UTMS
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--testcase", type=str, choices=ALL_UTMS.keys())
parser.add_argument("--precision", type=str, default="double")
args = parser.parse_args()


utm = ALL_UTMS[args.testcase]
print(utm)

graph = utm.get_fqir(bw_conf=args.precision)
print(graph.subgraphs["ARITH"])
utm.test_fqir_runtime(bw_conf=args.precision)
