install_dssr:
	mkdir -p helper/rna_angles_prediction_dssr
	git clone https://github.com/EvryRNA/rna_angles_prediction_dssr.git --branch preprocessing helper/rna_angles_prediction_dssr
	make -C /app/helper/rna_angles_prediction_dssr/dssr/src/
run:
	python -m src.rna_torsion_a_cli --in_pdb=data/preds/3drna_rp11.pdb --out_path=data/out.csv
run_all:
	python -m src.rna_torsion_a_cli --in_pdb=data/preds --out_path=data/out.csv
run_mae:
	python -m src.mae_metric_cli --pred_path=data/preds --native_path=data/rp11.pdb --out_path=data/out_mae.csv

docker_run:
	docker build -t rna_torsion_a .
	docker run --rm -it rna_torsion_a