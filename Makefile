install_dssr:
	mkdir -p helper/rna_angles_prediction_dssr
	git clone https://github.com/EvryRNA/rna_angles_prediction_dssr.git --branch preprocessing helper/rna_angles_prediction_dssr
run:
	python -m src.rna_torsion_a_cli --in_pdb=data/preds/3drna_rp11.pdb --out_path=data/out.json
run_all:
	python -m src.rna_torsion_a_cli --in_pdb=data/preds --out_path=data/out.json

docker_run:
	docker build -t rna_torsion_a .
	docker run --rm -it rna_torsion_a