import argparse
import json


parser = argparse.ArgumentParser(
    prog="microBlockz",
    description="Generates forge microblock config from tellMe block dumps.",
)

parser.add_argument("dump_filename")
parser.add_argument("blocklist_filename")
parser.add_argument("output_filename")


def load_dump(path):
    with open(path, "r") as f:
        return json.loads(f.read())


def load_blocklist(path):
    with open(path, "r") as f:
        return [block.strip() for block in f.readlines()]


def is_sequential(nums):
    return sorted(nums) == list(range(min(nums), max(nums) + 1))


def write_block_to_output(block_name, block_data, file):
    items = block_data.get("Item", [])

    if isinstance(items, dict):
        items = [items]

    variants = [item["ItemMeta"] for item in items]

    if variants and not is_sequential(variants):
        print(
            f"Block {block_name} has variants {variants} which do not seem to be sequential."
        )
        print(
            "I was too lazy to implement this, so you will need to do that range by hand, sorry!"
        )

    # xtones blocks don't store their variants normally I guess
    if "xtones:" in block_name and "lamp_flat" not in block_name:
        file.write(f'"{block_name}":0-15\n')
    elif len(variants) <= 1:
        file.write(f'"{block_name}"\n')
    else:
        file.write(f'"{block_name}":{min(variants)}-{max(variants)}\n')


def parse_args():
    args = parser.parse_args()

    dump_path = f"./{args.dump_filename}"
    blocklist_path = f"./{args.blocklist_filename}"
    output_path = f"./{args.output_filename}"

    return dump_path, blocklist_path, output_path


if __name__ == "__main__":
    # Reads the `dump` extracting all items whose names appear in the
    # `blocklist` and writes valid microblocks.cfg data to `output`.
    dump_path, blocklist_path, output_path = parse_args()

    dump = load_dump(dump_path)
    blocklist = load_blocklist(blocklist_path)

    with open(output_path, "w") as f:
        # The top level in the output is "AbyssalCraft": {...},
        for mod_name, mod_data in dump.items():
            # `categories` are blocks with metadata and an `Item` array||object
            for block_name, block_data in mod_data.items():
                if block_name in blocklist:
                    write_block_to_output(block_name, block_data, f)
