from pathlib import Path
from typing import Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
import json

from cardinal.api import cardinal_data_request
from .generate_test_data import DataGenerator
from .logger import request_logged
from rest_framework import permissions
from rest_framework.request import Request
from pathlib import Path
from cardinal.api import CARDINAL_VERSION
from .logger import _FILE_PATH, request_logged


CARDINAL_EMOJI = "🐦"


class VersionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        return Response(CARDINAL_VERSION, status=status.HTTP_200_OK)


class InitialApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        """Return a cardinal"""
        return Response(CARDINAL_EMOJI, status=status.HTTP_200_OK)


class CollectionDataRequestApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        collection_name = kwargs["collection_name"]

        # Returns all the database documents that have not been sent
        data = cardinal_data_request.get_unsent_docs(collection_name)

        # If test requested, overwrite test data
        if "test" in request.query_params:
            try:
                file = open(f"cardinal/api/hardcoded_test_data/{collection_name}.json")
                data = json.loads(file.read())
                file.close()
            except FileNotFoundError:
                return Response(
                    f"Test {collection_name} data not found.",
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(data, status=status.HTTP_200_OK)

class GetNotesApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        team_number: Optional[str] = kwargs["team_number"]
        if (team_number is None) or (team_number == ""):
            return Response({"success": False, "message": "No team number provided."}, status=status.HTTP_400_BAD_REQUEST)
        if not team_number.isnumeric():
            return Response({"success": False, "message": "Team number must be numeric."}, status=status.HTTP_400_BAD_REQUEST)

        team_number = kwargs["team_number"]
        return Response({"success": True, "notes": cardinal_data_request.get_notes(team_number)})

class SetNotesApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def post(self, request: Request, *args, **kwargs):
        if (not request.data) or (not request.data.get("team_number")) or (not request.data.get("notes")):
            return Response(
                "Missing team_number or notes in request body.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        team_number = request.data.get("team_number")
        if not team_number.isnumeric():
          return Response({"success": False, "message": "Team number must be numeric."}, status=status.HTTP_400_BAD_REQUEST)
        notes = request.data.get("notes")
        return Response({"success": cardinal_data_request.create_or_update_notes(team_number, notes)})

class SupportedCollectionsApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        return Response(cardinal_data_request.COLLECTIONS, status=status.HTTP_200_OK)


class TestDataGeneratorApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):

        filename = kwargs["data_structure_type"] + ".yml"
        generate_test_data = DataGenerator(filename)

        # If the "count" is specified, give that number to the data generator
        # Example "api/generate/calc_tba_team_schema/?format=json&count=10"
        if "count" in request.query_params:
            count = int(request.query_params["count"])
        else:
            count = 1

        if Path(f"schema/{filename}").exists():
            return Response(generate_test_data.get_data(count), status=status.HTTP_200_OK)
        else:
            return Response(f"The schema file {filename} doesn't exist.", status=status.HTTP_200_OK)


class MatchScheduleApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        comp_code = kwargs["comp_code"]
        data = cardinal_data_request.get_match_schedule(comp_code)

        return Response(data, status=status.HTTP_200_OK)


class TeamsListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        comp_code = kwargs["comp_code"]
        data = cardinal_data_request.get_teams_list(comp_code)

        return Response(data, status=status.HTTP_200_OK)


class LogFileApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        try:
            with open(_FILE_PATH, 'r') as log_file:
                return Response(log_file.read(), status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response('No log file data available.', status=HTTP_404_NOT_FOUND)
