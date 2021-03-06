import argparse

from taxumap.custom_logging import setup_logger
from taxumap.taxumap_base import Taxumap

if __name__ == "__main__":
    """Please use a '/' delimiter for weights and agg_levels"""

    parser = argparse.ArgumentParser(description="Get options for taxumap run")

    parser.add_argument(
        "-m", "--microbiota_data", help="Microbiota (rel_abundances) Table"
    )
    parser.add_argument("-t", "--taxonomy", help="Taxonomy Table")
    parser.add_argument("-w", "--weights", help="Weights")
    parser.add_argument("-a", "--agg_levels", help="Aggregation Levels")
    parser.add_argument("-s", "--save", help="Set Save to True or False")
    parser.add_argument("-o", "--outdir", help="Set directory to save embedding csv")

    parser.add_argument("-n", "--neigh", help="Sets the neighbors parameter for UMAP")
    parser.add_argument("-b", "--min_dist", help="Sets the min_dist parameter for UMAP")

    parser.add_argument(
        "-v",
        "--verbose",
        help="To get logging at info level and higher",
        action="count",
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="To get logging at debug level and higher",
        action="count",
    )

    args = parser.parse_args()

    inputs = {}
    transform_inputs = {}

    # # setup logger
    # # for verbose
    # if args.verbose:
    #     logger = setup_logger("run_taxumap", verbose=True)
    # else:
    #     logger = setup_logger("run_taxumap")

    # # for debug
    # if args.debug:
    #     logger = setup_logger("run_taxumap", debug=True)
    # else:
    #     logger = setup_logger("run_taxumap")

    # for neigh
    if args.neigh is not None:
        try:
            transform_inputs["neigh"] = int(args.neigh)
        except:
            logger.warning("--neigh/-n must be an integer")

    # for min_dist
    # TODO: Are there any other requirements for `min_dist`?
    if args.min_dist is not None:
        try:
            transform_inputs["min_dist"] = float(args.min_dist)
        except:
            logger.warning("--min_dist/-n must be a float")

    if args.save is not None:
        if "True" in args.save:
            save = True
        elif "False" in args.save:
            save = False
    else:
        save = True

    # AGG_LEVELS
    if args.agg_levels is not None:
        inputs["agg_levels"] = list(
            map(lambda x: x.capitalize(), args.agg_levels.split("/"))
        )

    # weights
    if args.weights is not None:
        weights = args.weights.split("/")
        inputs["weights"] = np.array(weights, dtype=np.float)

    # taxonomy
    if args.taxonomy is not None:
        inputs["taxonomy"] = args.taxonomy
    else:
        inputs["taxonomy"] = "./data/taxonomy.csv"

    # rel_abundances
    if args.microbiota_data is not None:
        inputs["microbiota_data"] = args.microbiota_data
    else:
        inputs["microbiota_data"] = "./data/microbiota_table.csv"

    if args.outdir is not None:
        inputs["outdir"] = args.outdir
    else:
        inputs["outdir"] = "./"

    print(inputs)
    print(transform_inputs)

    taxumap = Taxumap(**inputs)
    taxumap.transform_self(**transform_inputs)
    taxumap.save_embedding(inputs["outdir"]+"embedding.csv")#transform_self(save=save, **transform_inputs)
