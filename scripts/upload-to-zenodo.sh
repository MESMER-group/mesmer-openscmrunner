#!/bin/bash
#
# Upload a new version of the protocol to Zenodo.
# The protocol is first downloaded from S3, so must be uploaded there
# first.
#

if [ -f .env ]
then
  # thank you https://stackoverflow.com/a/20909045
  echo "Reading .env file"
  export $(grep -v '^#' .env | xargs)
fi

ROOT_DIR=$(dirname "$0")/..
SRC_DATA_DIR=$ROOT_DIR
ZENODO_JSON_FILE="${ROOT_DIR}/.zenodo.json"
DEPOSITION_ID_OLD="5094380"

# read version out of git
VERSION=$(git tag --points-at HEAD)

if [ -z "$VERSION" ]
then
    echo "No version tagged, exiting"
    exit 1
else
    echo "version: ${VERSION}"
fi

if [ -z "$ROOT_DIR_TO_STRIP" ]
then
    echo "No root directory to strip defined, exiting"
    exit 1
else
    echo "Will strip this from the start of found filenames: ${ROOT_DIR_TO_STRIP}"
fi

# put the correct version in .zenodo.json
sed -i -e "s/autofill-from-script-version/${VERSION}/g" "${ZENODO_JSON_FILE}"


DEPOSITION_ID=$(openscm-zenodo create-new-version "${DEPOSITION_ID_OLD}" "${ZENODO_JSON_FILE}" --zenodo-url zenodo.org)

BUCKET_ID=$(openscm-zenodo get-bucket ${DEPOSITION_ID} --zenodo-url zenodo.org)
echo "bucket id: ${BUCKET_ID}"


find . -not -path '*/\.*' -not -path '*egg-info*' -not -name '*.pyc' -not -name '*.pyc' -type f -exec bash -c 'openscm-zenodo upload --zenodo-url zenodo.org --root-dir "$2" "$0" "$1"' {} "${BUCKET_ID}" "${ROOT_DIR_TO_STRIP}" \;
