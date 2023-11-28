def get_package_location():
    import ailab
    dir_name = os.path.dirname(os.path.dirname(ailab.__file__))
    return dir_name


import os
import shutil
def create_and_copy_directories(data, base_dir, wrapper_dir="wrappers"):
    for category, subcategories in data.items():
        category_dir = os.path.join(base_dir, wrapper_dir, category)
        os.makedirs(category_dir, exist_ok=True)

        subcategory_before_path = get_package_location()
        for subcategory, subcategory_path in subcategories.items():
            subcategory_path = os.path.join(subcategory_before_path, subcategory_path)
            wrapper_path = os.path.join(subcategory_path, "wrapper.py")
            if os.path.exists(wrapper_path):
                shutil.copy(wrapper_path, category_dir)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="An example script with command-line arguments.")
    parser.add_argument("--workdir", type=str, default=None)
    args = parser.parse_args()

    if not args.workdir:
        raise SystemExit(f"workdir cannot None")

    if not os.path.exists(args.workdir):
        # 如果目录不存在，则创建目录
        os.makedirs(args.workdir)

    import json
    json_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(json_path,"config.json")
    with open(json_path, "r") as json_file:
        json_data = json.load(json_file)
        create_and_copy_directories(json_data, args.workdir)