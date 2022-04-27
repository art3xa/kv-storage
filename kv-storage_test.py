import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("--key", help='Key of the element')
parser.add_argument("--val", help='Value of the element')
args = parser.parse_args()

storage_path = os.path.join('data.data')

if os.path.isfile(storage_path):
    if args.val:
        with open(str(storage_path), "r") as f:
            m = json.load(f)
            if args.key in m:
                m[args.key] = m[args.key] + [args.val]
            else:
                m.update({args.key: [args.val]})
        with open(str(storage_path), "w") as f:
            json.dump(m, f)
    else:
        try:
            with open(str(storage_path), "r") as f:
                m = json.load(f)
                if m[args.key] == None:
                    print(None)
                if len(m[args.key]) > 1:
                    print(', '.join(m.get(args.key)))
                else:
                    print(*m.get(args.key))
        except:
            print(None)
else:
    d = {}
    with open(str(storage_path), "w") as f:
        if args.val:
            d = {args.key: [args.val]}
            json.dump(d, f)
        else:
            d = {args.key: None}
            print(None)

