# ENA Drag and Drop Submission

This pipeline allows you to do the entire submission process (project submission, sample submission, read submission, and genome assembly submission) after using the drag-and-drop method

## Prerequisite:

cx_Oracle : https://www.geeksforgeeks.org/how-to-install-cx_oracle-in-python-on-windows/

```
pip install cx_oracle
```
OR
```
conda install cx_oracle
```

## Installation

```
git clone https://github.com/KhadimGueyeKGY/ENA-drag_and_drop_submission.git
```

## Configuration
```
cd ENA-drag_and_drop_submission
export ORACLE_HOME=modules/instantclient_21_8/
export LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH
export PATH=$ORACLE_HOME:$PATH
export ORACLE_CLIENT_LIB=$ORACLE_HOME
source $HOME/.bashrc
```

## Usage

```
python drag_and_drop.py
```

After running this command, it will ask you a number of questions which are for examlpe:
  * $ Your OPS$USER > ops$khadim
  * $ Enter you OPS password >
  * $ enter the super user password >
  * $ Webin_account > Webin-xxxxxx
  * $ Do you use ENA test server for submission? [yes/no] > yes
  * $ path for the metadata spreadsheet (On excel file format) > data/uploader_tool_metadata_v5_genome_assemblies.xlsx
  * $ Specify the type of action needed ( ADD or MODIFY) > ADD






