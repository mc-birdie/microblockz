import argparse
import json


parser = argparse.ArgumentParser(
    prog="microBlockz",
    description="Generates forge microblock config from tellMe block dumps.",
)

parser.add_argument("dump_filename")
parser.add_argument("blocklist_filename")
parser.add_argument("output_filename")

metadata_overrides = {
    "biomesoplenty:gem_block": "0-7",
    "biomesoplenty:leaves_0": "8-11",
    "biomesoplenty:leaves_1": "8-11",
    "biomesoplenty:leaves_2": "8-11",
    "biomesoplenty:leaves_3": "8-11",
    "biomesoplenty:leaves_4": "8-11",
    "biomesoplenty:leaves_5": "8-11",
    "biomesoplenty:leaves_6": "8-9",
    "biomesoplenty:planks_0": "0-15",
    "biomesoplenty:log_0": "4-7",
    "biomesoplenty:log_1": "4-7",
    "biomesoplenty:log_2": "4-7",
    "biomesoplenty:log_3": "4-7",
    "biomesoplenty:log_4": "4-5",
}


def load_dump(path):
    with open(path, "r") as f:
        return json.loads(f.read())


def load_blocklist(path):
    with open(path, "r") as f:
        return [block.strip() for block in f.readlines()]


def is_sequential(nums):
    return sorted(nums) == list(range(min(nums), max(nums) + 1))


def get_sequence_string(nums):
    return ",".join(str(n) for n in sorted(nums))


def write_block_to_output(block_name, block_data, file):
    items = block_data.get("Item", [])

    if isinstance(items, dict):
        items = [items]

    variants = [item["ItemMeta"] for item in items]

    if variants and not is_sequential(variants):
        sequence = get_sequence_string(variants)
        file.write(f'"{block_name}":{sequence}\n')

    # xtones blocks don't store their variants normally I guess
    if "xtones:" in block_name and "lamp_flat" not in block_name:
        file.write(f'"{block_name}":0-15\n')
    elif block_name in metadata_overrides.keys():
        file.write(f'"{block_name}":{metadata_overrides[block_name]}\n')
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
