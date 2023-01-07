from venv import create
from TripletSearchConNorm.TripletSearchConNorm.model.concept_normalizer import ConceptNormalizer
import argparse
import pandas as pd


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', help="path trained model")
    parser.add_argument('--data_path', '-d', help='path to data')
    parser.add_argument('--ontology_path', '-onto', help='path to ontology')
    parser.add_argument('--output_path', '-o', help='output of predictions')

    return parser

def main(args):
    normalizer = ConceptNormalizer(model_name_or_path=args.model)
    normalizer.load_ontology(args.ontology_path)

    df = pd.read_csv(args.data_path)

    output_data = []

    for tuplerow in df.itertuples():

        normalized_entity = normalizer.normalize(tuplerow[0], top_k=1)

        output_data.append((tuplerow[0], normalized_entity[0]))
    
    outdf = pd.DataFrame(output_data, columns =['Entity', 'CUI'])

    outdf.to_csv(args.output_path)


if __name__=="__main__":
    parser = create_parser()
    args = parser.parse_args()

    main(args)

