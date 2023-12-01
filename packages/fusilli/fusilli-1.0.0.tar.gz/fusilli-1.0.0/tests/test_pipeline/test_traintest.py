import pytest
from fusilli.data import get_data_module
from fusilli.train import train_and_save_models
from fusilli.utils.model_chooser import import_chosen_fusion_models
from fusilli.eval import ConfusionMatrix
from ..test_data.test_TrainTestDataModule import create_test_files


@pytest.mark.filterwarnings("ignore:.*does not have many workers*.", )
@pytest.mark.filterwarnings("ignore:.*The number of training batches*.")
@pytest.mark.filterwarnings("ignore:.*No positive samples in targets,*.")
@pytest.mark.filterwarnings("ignore:.*No negative samples in targets,*.")
@pytest.mark.filterwarnings("ignore:.*exists and is not empty*.")
def test_train_and_test(create_test_files, tmp_path):
    # model_conditions = {"class_name": ["Tabular1Unimodal"]}
    model_conditions = {"modality_type": "all"}
    fusion_models = import_chosen_fusion_models(model_conditions, skip_models=["MCVAE_tab"])

    tabular1_csv = create_test_files["tabular1_csv"]
    tabular2_csv = create_test_files["tabular2_csv"]
    image_torch_file_2d = create_test_files["image_torch_file_2d"]

    loss_fig_path = tmp_path / "loss_fig_path"
    loss_fig_path.mkdir()

    loss_log_dir = tmp_path / "loss_log_dir"
    loss_log_dir.mkdir()

    local_fig_path = tmp_path / "local_fig_path"
    local_fig_path.mkdir()

    checkpoint_dir = tmp_path / "checkpoint_dir"
    checkpoint_dir.mkdir()

    modifications = {
        "AttentionAndSelfActivation": {"attention_reduction_ratio": 2}
    }

    params = {
        "test_size": 0.2,
        "pred_type": "binary",
        "multiclass_dims": None,
        "kfold_flag": False,
        "tabular1_source": tabular1_csv,
        "tabular2_source": tabular2_csv,
        "img_source": image_torch_file_2d,
        "log": False,
        "loss_fig_path": str(loss_fig_path),
        "loss_log_dir": str(loss_log_dir),
        "local_fig_path": str(local_fig_path),
        "checkpoint_dir": str(checkpoint_dir),
    }

    for model in fusion_models:
        dm = get_data_module(fusion_model=model, params=params, layer_mods=modifications, max_epochs=2)

        single_model_list = train_and_save_models(
            data_module=dm,
            params=params,
            fusion_model=model,
            max_epochs=2,
            enable_checkpointing=False,
            layer_mods=modifications,
        )

        trained_model = single_model_list[0]

        assert trained_model is not None
        assert trained_model.model is not None

        fig = ConfusionMatrix.from_final_val_data([trained_model])
        assert fig is not None
