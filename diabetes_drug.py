import pickle
from chembl_webresource_client.new_client import new_client
import pandas as pd
from padelpy import from_smiles
model=pickle.load(open("diabetes.pkl","rb"))
def choices():
    choice=input("Enter 1 to directly input smiles      or       Enter 2 to input chembl id : " )
    if choice=="1":
        smiles=input("enter smiles notation : ")
        print("#" * 181)
        print(predictions(smiles))
        print("#" * 181)
    if choice=="2":
        chembl_id=input("enter chembl id : ")
        print("#"*181)
        print(preprocess(chembl_id))
        print("#" * 181)
    else:
        print("invalid input")

def preprocess(drug_id):
    molecule = new_client.molecule
    drug_candidate = molecule.filter(chembl_id=drug_id).only(['molecule_chembl_id', 'molecule_structures'])
    if len(drug_candidate)==0:return "smiles not found in chembl database"
    drug_candidate_smiles=drug_candidate[0]['molecule_structures']['canonical_smiles']
    return predictions(drug_candidate_smiles)

def predictions(smiles):
    try:
        descriptors=from_smiles(smiles, fingerprints=True, descriptors=False)
    except:
        return "invalid smiles notation"
    df = pd.DataFrame(data=descriptors.values(), index=descriptors.keys())
    df=df.T     #transpose current df
    predicted_value=model.predict(df)[0]
    return f"predicted value : {predicted_value}"

choices()
