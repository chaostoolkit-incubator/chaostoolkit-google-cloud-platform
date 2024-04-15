from unittest.mock import MagicMock, patch, ANY

from chaosgcp.cloudlogging.controls import journal as journal_ctrl

import fixtures


@patch("chaosgcp.cloudlogging.controls.journal.gcp_logging", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_journal_ctrl_send_logs(Credentials, gcp_logging) -> None:
    Credentials.from_service_account_file.return_value = MagicMock()

    logging_client = MagicMock()
    gcp_logging.Client.return_value = logging_client
    logger = MagicMock()
    logging_client.logger.return_value = logger

    x = {"title": "hello"}

    j = {"status": "succeeded"}

    lbls = {"location": "us-west1"}

    journal_ctrl.after_experiment_control(
        context=x, state=j, configuration=fixtures.configuration
    )

    logger.log_struct.assert_called_with(info=j, insert_id=ANY, labels=lbls)


@patch("chaosgcp.cloudlogging.controls.journal.gcp_logging", autospec=True)
@patch("chaosgcp.Credentials", autospec=True)
def test_journal_ctrl_send_logs_with_labels(Credentials, gcp_logging) -> None:
    Credentials.from_service_account_file.return_value = MagicMock()

    logging_client = MagicMock()
    gcp_logging.Client.return_value = logging_client
    logger = MagicMock()
    logging_client.logger.return_value = logger

    x = {"title": "hello"}

    j = {"status": "succeeded"}

    lbls = {"appid": "123", "location": "us-west1"}

    journal_ctrl.after_experiment_control(
        context=x, state=j, labels=lbls, configuration=fixtures.configuration
    )

    logger.log_struct.assert_called_with(info=j, insert_id=ANY, labels=lbls)
