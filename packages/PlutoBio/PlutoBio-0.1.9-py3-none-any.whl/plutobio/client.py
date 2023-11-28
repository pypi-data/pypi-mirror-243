import requests
from typing import Union
import os
import uuid

from .plots import Plot, Plots, Displays, Display
from .assay_data import AssayData
from .sample_data import SampleData
from .analyses import Analysis
from .attachments import Attachment
from .pipelines import Pipelines
from .projects import Project
from .results import Results
from .experiments import Experiment, Experiments
from .download_upload import DownloadUploadHandler
from .settings import DEFAULT_TMP_PATH
import pandas as pd
from . import utils


class PlutoClient:
    """Base class for Pluto API access"""

    def __init__(self, token: str, test_client=None) -> None:
        self._experiment = Experiment(client=self)
        self._plots = Plot(client=self)
        self._assay_data = AssayData(client=self)
        self._sample_data = SampleData(client=self)
        self._attachment = Attachment(client=self)
        self._analysis = Analysis(client=self)
        self._pipelines = Pipelines(client=self)
        self._project = Project(client=self)
        self._results = Results(client=self)
        self._download_upload = DownloadUploadHandler(client=self)
        self._plot_displays = Display(client=self)
        self._token = token
        self._base_url = os.environ.get("PLUTO_API_URL", "https://api.pluto.bio")
        self._test_client = test_client

    def _handle_response_errors(self, response) -> None:
        """Handle HTTP errors based on the response status code.

        :param response: The HTTP response.
        :type response: requests.Response
        :raises HTTPError: With a specific message based on the status code.
        """
        response_content = response.json()
        error_message = f"Response: {response.status_code} - {response.status_text} | Message: {response_content['message']} | Code ID: {response_content['code']} | Additional details: {response_content['details']}"

        if response.status_code == 400:
            raise requests.HTTPError(error_message)
        elif response.status_code == 401:
            raise requests.HTTPError(error_message)
        elif response.status_code == 403:
            raise requests.HTTPError(error_message)
        elif response.status_code == 404:
            raise requests.HTTPError(error_message)
        elif response.status_code == 500:
            raise requests.HTTPError(error_message)
        else:
            raise requests.HTTPError(error_message)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ) -> dict:
        """
        Make a generic HTTP request to the API.

        :param method: HTTP method (e.g., GET, POST, PUT, DELETE).
        :type method: str
        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param params: Query parameters to be included in the request, defaults to None.
        :type params: dict, optional
        :param data: JSON data to be sent in the request body, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the request to the API is not successful.
        """
        url = f"{self._base_url}/{endpoint}/"

        # For django testing we need to use the django client
        if self._test_client:
            request_headers = {
                "HTTP_AUTHORIZATION": f"Token {self._token}",
            }

            if headers is not None:
                request_headers.update(headers)

            if method == "GET":
                response = self._test_client.get(
                    url, data=data, content_type="application/json", **request_headers
                )
            elif method == "POST":
                response = self._test_client.post(
                    url, data=data, content_type="application/json", **request_headers
                )
            elif method == "DELETE":
                response = self._test_client.delete(
                    url, data=data, content_type="application/json", **request_headers
                )
            elif method == "PUT":
                response = self._test_client.put(
                    url, data=data, content_type="application/json", **request_headers
                )
            elif method == "PATCH":
                response = self._test_client.patch(
                    url, data=data, content_type="application/json", **request_headers
                )

        else:
            request_headers = {
                "AUTHORIZATION": f"Token {self._token}",
            }

            response = requests.request(
                method, url, params=params, json=data, headers=request_headers
            )

        # Raise an exception if the status code is not 200 or 201
        if response.status_code != 200 and response.status_code != 201:
            self._handle_response_errors(response)

        return response.json()

    def get(self, endpoint: str, data: dict = None, params: dict = None) -> dict:
        """
        Make a GET request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param params: Query parameters to be included in the GET request, defaults to None.
        :type params: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the GET request to the API is not successful.
        """
        return self._make_request("GET", endpoint, params=params, data=data)

    def post(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a POST request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the POST request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the POST request to the API is not successful.
        """
        return self._make_request("POST", endpoint, data=data)

    def delete(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a DELETE request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the DELETE request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the DELETE request to the API is not successful.
        """
        return self._make_request("DELETE", endpoint, data=data)

    def put(self, endpoint: str, data: dict = None, headers: dict = None) -> dict:
        """
        Make a PUT request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the PUT request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the PUT request to the API is not successful.
        """
        return self._make_request("PUT", endpoint, data=data, headers=headers)

    def patch(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a PATCH request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the PATCH request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the PATCH request to the API is not successful.
        """
        return self._make_request("PATCH", endpoint, data=data)

    def list_projects(self):
        return self._project.list()

    def get_project(self, project_id: Union[str, uuid.UUID]):
        """Retrieves details for a specific project based on its uuid or pluto ID.

        Args:
            project_id (str or uuid): The pluto id or object uuid of the project to retrieve.

        Returns:
            Project Object: Project object.
        """
        return self._project.get(project_id=project_id)

    def list_experiments(self) -> Experiments:
        """Lists all projects.

        Returns:
            list: List of projects.
        """
        return self._experiment.list()

    def get_experiment(self, experiment_id: Union[str, uuid.UUID]) -> Experiment:
        """Retrieves details for a specific project based on its uuid or pluto ID.

        Args:
            experiment_id (str or uuid): The pluto id or object uuid of the experiment to retrieve.

        Returns:
            dict: Experiment details.
        """
        return self._experiment.get(experiment_id)

    def list_plots(self, experiment_id: Union[str, uuid.UUID]) -> Plots:
        """Retriveves a list for all plots inside an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Pluto ID or Experiment UUID

        Returns:
            Plots: Returns a list of Plots
        """
        return self._plots.list(experiment_id)

    def get_plot(
        self, experiment_id: Union[str, uuid.UUID], plot_id: Union[str, uuid.UUID]
    ) -> Plot:
        """Retrieves a plot from an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            plot_id (Union[str, uuid.UUID]): Plot UUID

        Returns:
            Plot: Returns a plot object
        """
        return self._plots.get(experiment_id=experiment_id, plot_id=plot_id)

    def get_plot_data(
        self,
        experiment_id: Union[str, uuid.UUID],
        plot_id: Union[str, uuid.UUID],
        folder_path: str = DEFAULT_TMP_PATH,
    ) -> pd.DataFrame:
        """Get the data from a specific plot. It returns the data that was used to generate that plot

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            plot_id (Union[str, uuid.UUID]): Plot UUID

        Returns:
            pd.DataFrame: Plot data as a dataframe
        """

        return self._plots.data(
            experiment_id=experiment_id, plot_id=plot_id, folder_path=folder_path
        )

    def get_assay_data(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ) -> pd.DataFrame:
        """Get the assay data from an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            folder_path (str, optional): Folder path to save the data. Defaults to /tmp.

        Returns:
            pd.DataFrame: Returns assay data as a pandas dataframe
        """
        return self._assay_data.get(experiment_id, folder_path=folder_path)

    def get_sample_data(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ) -> pd.DataFrame:
        """Get the sample data from an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            folder_path (str, optional): Folder path to save the data. Defaults to /tmp.

        Returns:
            pd.DataFrame: Returns sample data as a pandas dataframe
        """
        return self._sample_data.get(experiment_id, folder_path=folder_path)

    def download_bam_files(
        self,
        experiment_id: Union[str, uuid.UUID],
        file_id: Union[str, uuid.UUID],
        folder_path: str = DEFAULT_TMP_PATH,
    ):
        """Download bam files from an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            file_id (Union[str, uuid.UUID]): BAM file UUID
            folder_path (str, optional): _description_. Defaults to DEFAULT_TMP_PATH.

        Returns:
            _type_: _description_
        """
        return self._pipelines.download_bam_files(
            experiment_id, file_id=file_id, folder_path=folder_path
        )

    def download_qc_report(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ):
        return self._pipelines.download_qc_report(experiment_id, folder_path)

    def list_attachments(self, experiment_id: Union[str, uuid.UUID]):
        return self._attachment.list(experiment_id)

    def download_attachments(
        self,
        experiment_id: Union[str, uuid.UUID],
        file_id: Union[str, uuid.UUID],
        folder_path: str = DEFAULT_TMP_PATH,
    ):
        return self._attachment.download(
            experiment_id, file_id, folder_path=folder_path
        )

    def add_plot(
        self,
        experiment_id: Union[str, uuid.UUID],
        plot_uuid: Union[str, uuid.UUID] = None,
        file_path: str = DEFAULT_TMP_PATH,
        data_or_analysis_uuid: str = None,
        methods_str_or_path: str = "",
    ):
        if plot_uuid is not None and data_or_analysis_uuid is not None:
            raise ValueError(
                "Both plot_uuid and data_or_analysis_uuid cannot be provided together."
            )

        # We support the user to add methods as a string or as a file
        methods = utils.get_content(methods_str_or_path)

        # Convert dataframe to csv file to be uploaded to gcs.
        display_uuid = ""
        # First step is to check if the user provided a plot_uuid. If the user provided a
        # plot_uuid then we want to get it's corresponding plot and analysis to be able to edit it.
        if plot_uuid is not None:
            plot = self._plots.get(experiment_id, plot_uuid)
            analysis_uuid = plot.analysis["uuid"]
            display_uuid = plot.display["uuid"]
        # If user did not specify the plot_uuid, then it means we want to create one.
        else:
            create_figure = self._plots.create(
                experiment_id=experiment_id,
                data={
                    "analysis_type": "external",
                    "display_type": "html",
                    "status": "published",
                },
            )

            display_uuid = create_figure.display["uuid"]

            plot_uuid = create_figure.uuid

            analysis_data = {
                "analysis_type": "external",
                "name": "{plot_uuid}_plot.html",
                "methods": methods,
            }

            analysis_uuid = ""

            if data_or_analysis_uuid is not None:
                if utils.is_valid_uuid(data_or_analysis_uuid):
                    create_figure = self._plots.update(
                        experiment_id=experiment_id,
                        plot_uuid=plot_uuid,
                        data={
                            "analysis_id": data_or_analysis_uuid,
                        },
                    )
                    analysis_uuid = data_or_analysis_uuid
                    # analysis_data["analysis_uuid"] = analysis_uuid
                    # analysis_data["results"] = f"{plot_uuid}_plot_data.csv"
                    # create_analysis = self._analysis.create(
                    #     experiment_id=experiment_id, data=analysis_data
                    # )
                else:
                    analysis_data["results"] = f"{plot_uuid}_plot_data.csv"

                    create_analysis = self._analysis.create(
                        experiment_id=experiment_id, data=analysis_data
                    )

                    analysis_uuid = create_analysis.uuid

            else:
                create_analysis = self._analysis.create(
                    experiment_id=experiment_id, data=analysis_data
                )
                analysis_uuid = create_analysis.uuid

            link_response = self._plots.link_analysis(
                experiment_id=experiment_id,
                analysis_id=analysis_uuid,
                display_id=display_uuid,
                plot_id=plot_uuid,
            )

        # Upload plot html file
        upload_response = self._download_upload.upload_file(
            experiment_id=experiment_id,
            file_path=file_path,
            data={
                "analysis_type": "external",
                "origin": "python",
                "filename": f"{analysis_uuid}/{plot_uuid}_plot.html",
                "data_type": "external",
                "file_type": os.path.splitext(os.path.basename(file_path))[1],
                "file_size": os.path.getsize(file_path),
            },
        )

        # Once ExternalAnalysis is created and the file is upload.
        # We need to link the uploaded file to the ExternalAnalysis
        response = self._plot_displays.update(
            experiment_id=experiment_id,
            plot_uuid=plot_uuid,
            display_uuid=display_uuid,
            data={
                "figure_file": upload_response["experiment_file"],
                "display_type": "external",
                "methods": methods,
                "analysis_id": analysis_uuid,
                "display_id": display_uuid,
            },
        )

        # If the user provided some data that they want to link to the plot. We
        # want to upload it
        if data_or_analysis_uuid is not None:
            if utils.is_valid_uuid(data_or_analysis_uuid):
                # response = self._analysis.update(
                #     experiment_id=experiment_id,
                #     analysis_uuid=analysis_uuid,
                #     data={"results": upload_response["experiment_file"]["uuid"]},
                # )
                pass
            else:
                with utils.dataframe_to_csv(
                    data_or_analysis_uuid, f"{plot_uuid}_plot_data.csv"
                ) as temp_file_path:
                    upload_post_data_response = self._download_upload.upload_file(
                        experiment_id=experiment_id,
                        data={
                            "analysis_type": "external",
                            "origin": "python",
                            "filename": f"{analysis_uuid}/{os.path.basename(temp_file_path)}",
                            "data_type": "external",
                            "file_type": os.path.splitext(
                                os.path.basename(temp_file_path)
                            )[1],
                            "file_size": os.path.getsize(temp_file_path),
                        },
                        file_path=temp_file_path,
                    )
                    response = self._analysis.update(
                        experiment_id=experiment_id,
                        analysis_uuid=analysis_uuid,
                        data={
                            "results": upload_post_data_response["experiment_file"][
                                "uuid"
                            ]
                        },
                    )

        # TODO: We need to add a safe for the upload response. In case it fails, we need to be able to
        # remove the analysis that we created

        # TODO: We need to have a post validation after files are uploaded

        # Update plots
        self._plots.update(
            experiment_id=experiment_id,
            plot_uuid=plot_uuid,
            data={"analysis_id": analysis_uuid},
        )

        # # Update analysis
        # response = self._analysis.update(
        #     experiment_id=experiment_id,
        #     analysis_uuid=analysis_uuid,
        #     data={"methods": methods},
        # )

        return response

    def download_file(
        self, experiment_id: Union[str, uuid.UUID], file_id: Union[str, uuid.UUID]
    ):
        return self._download_upload.download_file(experiment_id, file_id)

    # def upload_file(
    #     self,
    #     experiment_id: Union[str, uuid.UUID],
    #     analysis_id: str = "",
    #     file_path: str = DEFAULT_TMP_PATH,
    # ):
    #     return self._download_upload.upload_file(
    #         experiment_id=experiment_id, analysis_id=analysis_id, file_path=file_path
    #     )
