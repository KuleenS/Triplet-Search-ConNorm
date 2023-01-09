import os
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
    normalizer = ConceptNormalizer(model_name_or_path=args.model, sentence_transformer=True)
    normalizer.load_ontology(args.ontology_path)

    df = pd.read_csv(args.data_path, sep="\|\|", names=["abstract_id", "offset", "type", "mention", "entity_ids"])

    df[['offset_start','offset_finish']] = df.offset.str.split(pat="|", expand=True)

    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'id'})

    df = df[["id", "abstract_id", "offset_start", "offset_finish", "type", "mention", "entity_ids"]]

    output_data = []

    for tuplerow in df.itertuples():

        normalized_entity = normalizer.normalize(tuplerow.mention, top_k=1)

        output_data.append(normalized_entity[0][0])
    
    df['entity_ids'] = output_data


    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path, exist_ok = True)

    df.to_csv(os.path.join(args.output_path, "TripletPreds.tsv"), sep = "\t", index = False)


if __name__=="__main__":
    parser = create_parser()
    args = parser.parse_args()

    main(args)

