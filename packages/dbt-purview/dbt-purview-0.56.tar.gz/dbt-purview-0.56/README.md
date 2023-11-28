**DBT (Data Build Tool)** is a popular open-source data transformation and modelling tool data professionals use to build and manage data pipelines. It allows users to define, test, and run data transformations in a modular and version-controlled way, promoting collaboration and consistency in data analytics and reporting.

Purview, on the other hand, is a data governance and cataloging service offered by Microsoft. It helps organizations discover, understand, and manage their data assets, ensuring data compliance, security, and lineage.

Our Python package is a powerful tool that simplifies the process of establishing robust data lineage and improving data governance within your organization, by seamlessly integrating with your data infrastructure and workflows.

**Required version**
DBT Core : 1.5 

**Step 1:** Install the Required Python Package
First, install the dbt-purview Python package using pip:

```pip install dbt-purview-integration==1.0```

Note: if you are using airflow with data factory then add  dbt-purview-integration==1.0 inside Airflow requirements.

**Step 2:** Configure Microsoft Purview
Create a Microsoft purview account and do a data source scan for the required data warehouse/database.

**Step 3:** Configure Microsoft Purview Connection in Airflow
In your Airflow DAG file, add configuration for the Microsoft Purview connection using the azure_purview connection ID. required details are cliend_id, client_secret, tenantId, resource(purview URL)

![Screenshot from 2023-11-07 16-29-09](https://github.com/ankitvalens/dbt-purview/assets/118506860/97e7d228-3235-41a4-958f-9d56446fc7c7)

**Step 4:** Configure the BashOperator to build lineage
In your DAG file, configure a BashOperator task to run after the completion of your dbt DAG or as a separate run. This task will execute the dbtpurview command to build lineage in Microsoft purview. Make sure to pass the appropriate parameters like --env, --dwhcid --path(manifest file path), and --azpurview.

    ```purview = BashOperator(
        task_id="purview",
        bash_command=f"dbtpurview --env=databricks --path={PROJECT_ROOT_PATH}/target" --dwhcid=databricks_connection_id --azpurview=azure_purview_connection_id,
        trigger_rule= "all_done"
    )```
this package will read manifest file from the given target folder and read data warehouse and Azure purview details from airflow connection then build lineage in your purview account.

**Limitations**
scanning is required to build lineage 
either user has to provide a manifest file or you can attach bashoperator at the end of the dbt run in dag


