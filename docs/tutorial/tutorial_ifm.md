# Using Automated Defect Analysis on IFM Images

This tutorial is to demonstrate how to perform an automated defect analysis on IFM images.  
To execute the analysis, there need to be three NOMAD entries present: 

* an IFM Measurement type entry with associated microscopy file
* two IFM Model type entries, each with the respective `.keras` model file

Depending on your knowledge and on which entries you have already present, you may jump ahead to the [IFM Analysis](#ifm-analysis) subsection. 

## Uploads

1. **NOMAD Uploads page**:  
    Navigate to your Uploads page, reachable under `PUBLISH > Uploads`.
2. **Enter upload**:  
    You might need to create a new new upload using  or edit an existing one.  
    ![Create or Edit Upload](../assets/tutorial_ifm/create_edit_upload.png)

## IFM Measurement Entry

1. **Create a new entry**:  
    Create a new entry via the button `Create from Schema`.  
    ![Create a new entry](../assets/tutorial_ifm/create_new_entry.png)
    Give it a name and select `IFM Measurement` as type.  
    ![Create a new IFM measurement entry](../assets/tutorial_ifm/create_new_entry_measurement.png)
2. **Assign the measurement files**:  
    You should now see the data section of the created entry. Assign an image and a metadata file.  
    ![Assign measurement files](../assets/tutorial_ifm/measurement_assign_files.png)
    Don't forget to click the save button in the top right corner afterwards!  
    ![Assign measurement files](../assets/tutorial_ifm/measurement_assign_files_save.png)
3. **Automated XML Parsing**:
    As soon as a XML file is assigned, the plugin extracts metadata from it, such as:
    * exposure time
    * start and end time
    * magnification

    ![Processed entry](../assets/tutorial_ifm/measurement_assign_files_processed.png)
    If you have a `UIBKSample` entry already present with the same `lab_id` as extracted from the XML file, the entry automatically creates a reference to it.  
    ![Reference to sample](../assets/tutorial_ifm/measurement_assign_files_reference.png)


## IFM Model

Perform the same steps as above for creating two `IFM Model` entries:

1. **Create a new entry**:  
    Create a new entry via the button `Create from Schema`.  
    ![Create a new entry](../assets/tutorial_ifm/create_new_entry.png)
    Give it a name and select `IFM Model` as type.  
    ![Create a new IFM model entry](../assets/tutorial_ifm/create_new_entry_model.png)
2. **Assign the measurement files**:  
    You should now see the data section of the created entry. Assign an image and a metadata file.  
    ![Assign measurement files](../assets/tutorial_ifm/model_assign_files.png)
    Don't forget to click the save button in the top right corner afterwards!  
    ![Assign measurement files](../assets/tutorial_ifm/model_assign_files_save.png)
3. **Automated Parsing**:
    As soon as the `.keras` file is assigned, the plugin extracts metadata from it, such as:
    * model type (binary/classification)
    * number of layers
    * number of parameters

    ![Processed entry](../assets/tutorial_ifm/model_assign_files_processed.png)
   

## IFM Analysis

At this point, your NOMAD upload should contain at least one `IFMMeasurement` entry and two `IFMModel` entries:

![Starting Point Analysis](../assets/tutorial_ifm/analysis_start.png)

To perform the analysis on this measurement perform the following steps: 

1. **Create a new IFMAnalysis entry**:  
    ![Create a new IFM analysis entry](../assets/tutorial_ifm/create_new_entry_analysis.png)
2. **Assign the measurement entry**:  
    Create a new `input` section by clicking the plus icon:  
    ![Create a new input](../assets/tutorial_ifm/analysis_reference_add.png)  
    Click on the pen icon to assign an existing entry:  
    ![Assign an existing entry](../assets/tutorial_ifm/analysis_reference_assign.png)  
    Select the IFMMeasurement entry you want to analyze:  
    ![Select the measurement entry](../assets/tutorial_ifm/analysis_reference_select.png)  
    Save this change:  
    ![Save changes](../assets/tutorial_ifm/analysis_reference_save.png)  
    ![Done](../assets/tutorial_ifm/analysis_reference_assigned.png)  
3. **Assign the models**:
    Repeat the steps from above to assign both `IFMModel` entries as well:  
    ![Ready](../assets/tutorial_ifm/analysis_ready.png)  
4. **Check 'perform analysis'**:  
    By opting the 'perform analysis' checkbox (and saving) the image analysis is triggered:  
    ![Perform analysis](../assets/tutorial_ifm/analysis_perform.png)  
5. **Results**:
    Execution of the code can take up to several minutes.
    Results are stored in a csv file that is referenced in the `output` section of the `IFMAnalsis` entry:  
    ![Results](../assets/tutorial_ifm/analysis_results_figure.png)
    From these results, a heatmap of the spatial distribution of detected defects is generated, and the prevalence of classified defects is calculated.  
    ![Results](../assets/tutorial_ifm/analysis_results_prevalence.png)  

