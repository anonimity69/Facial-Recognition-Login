import argparse
from utils.collector import FaceCollector

def main():
    parser = argparse.ArgumentParser(description="Facial Image Collector")
    parser.add_argument("--user", required=True, help="User's name")
    parser.add_argument("--count", type=int, default=100, help="Number of images to collect")
    args = parser.parse_args()

    collector = FaceCollector(user_name=args.user, num_images=args.count)
    collector.collect()

if __name__ == "__main__":
    main()
