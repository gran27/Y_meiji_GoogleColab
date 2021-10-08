import argparse
from tools.eval import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluation for mouse Y_meiji experiment."
    )
    parser.add_argument(
        "file",
        type=str,
        help="video file path (ex: ./data/01504.MTS)",
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=["csv", "txt"],
        default="csv",
        help="format of output file",
    )
    parser.add_argument(
        "--shift",
        type=float,
        default=0,
        help="video shift",
    )
    parser.add_argument(
        "--outspeed",
        type=int,
        default=1,
        help="X speed for output video file",
    )
    parser.add_argument(
        "--yth",
        type=float,
        default=0.1,
        help="If smaller, accuracy to find Y-meiji edges is better (Default: 0.1)",
    )
    parser.add_argument(
        "--weights", type=str, default="model/best.pt", help="model path"
    )
    args = parser.parse_args()
    main(args)
