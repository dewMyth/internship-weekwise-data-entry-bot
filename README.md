### Step 1 - Create the Week

Run the following command to create a new week starting from 2025-07-07:

```bash
python add_week.py --email xxxxxxxxxxx@stu.kln.ac.lk --password xxxxxx --start 2025-07-07
```

> **Note:** 2025-07-07 is the start date of the week. Adjust it as needed. (This will be same for the following instructions as well)

### Step 2 - Prepare the CSV file for that week

Rename it to `day_records_2025-07-07.csv` and ensure it has the following columns:

> **Note:** Using the `day_records_2025-07-07.csv` file as a template is recommended.

### Step 3 - Fill the CSV file week wise with the following columns:

```csv
| Date       | Organization Category | Experience Category | Sub Job Experience Category | Student Contribution | Computerized Work Hours | Manual Work Hours | Remarks                       |
| ---------- | --------------------- | ------------------- | --------------------------- | -------------------- | ----------------------- | ----------------- | ----------------------------- |
| 2025-07-07 | 5                     | 415                 | 416                         | 1                    | 2                       | 1                 | Finished API documentation.   |
| 2025-07-07 | 2                     | 415                 | 416                         | 1                    | 2                       | 3                 | Finished API documentation 2. |
| 2025-07-08 | 1                     | 415                 | 416                         | 1                    | 5                       | 3                 | UI done                       |
| 2025-07-09 | 1                     | 415                 | 416                         | 1                    | 6                       | 2                 | DB designed                   |
| 2025-07-10 | 1                     | 415                 | 416                         | 1                    | 2                       | 6                 | Feedback noted                |
| 2025-07-11 | 1                     | 415                 | 416                         | 1                    | 3                       | 5                 | Bugs fixed                    |

```

Guide to fill the CSV file (For Dropdown values only):
| **Value** | **Organization Category** |
| --------- | -------------------------------------------------- |
| 1 | Manufacturing |
| 2 | Banking / Finance / Insurance |
| 3 | Engineering |
| 4 | Agriculture / Fisheries / Mining |
| 5 | Transport / Energy / Health / Educational Services |
| 6 | Retail / Wholesale Trade |
| 7 | Hotels |
| 8 | Not for Profit organizations |
| 9 | Others |

| **Value** | **Experience Category**                      |
| --------- | -------------------------------------------- |
| 415       | Business Information Systems                 |
| 432       | Business Reporting                           |
| 449       | Management, Compliance, Assurance and Ethics |
| 465       | Finance & Economics                          |

### Sub-Experience Category Mapping

| **Value** | **Code** | **Sub-Experience Category**           |
| --------- | -------- | ------------------------------------- |
| 416       | BIS1     | Requirements Gathering                |
| 417       | BIS2     | Functional Analysis                   |
| 418       | BIS3     | Data Analysis                         |
| 419       | BIS4     | Use-Case Development                  |
| 420       | BIS5     | System Design Support                 |
| 421       | BIS6     | User Acceptance Testing               |
| 422       | BIS7     | Interface Design                      |
| 423       | BIS8     | Process Mapping and Redesign          |
| 424       | BIS9     | Change Management                     |
| 425       | BIS10    | Requirements Prioritization           |
| 426       | BIS11    | Data Migration Planning               |
| 427       | BIS12    | Risk Identification                   |
| 428       | BIS13    | Project Coordination                  |
| 429       | BIS14    | Documentation Management              |
| 430       | BIS15    | Stakeholder Engagement                |
| 431       | BIS16    | Continuous Learning                   |
| 433       | BR1      | Data Collection                       |
| 434       | BR2      | Data Cleansing and Validation         |
| 435       | BR3      | Financial Report Generation           |
| 436       | BR4      | Financial Analysis                    |
| 437       | BR5      | Variance Analysis                     |
| 438       | BR6      | Budgeting and Forecasting Support     |
| 439       | BR7      | BR7 Data Visualization                |
| 440       | BR8      | Report Customisation                  |
| 441       | BR9      | Ad Hoc Analysis                       |
| 442       | BR10     | Financial Statement Review            |
| 443       | BR11     | Financial Compliance                  |
| 444       | BR12     | Trend Identification                  |
| 445       | BR13     | Communication                         |
| 446       | BR14     | Process Improvement                   |
| 447       | BR15     | Cross-functional Collaboration        |
| 448       | BR16     | Learning and Professional Development |
| 450       | MCAE1    | Ethics and Code of Conduct            |
| 451       | MCAE2    | Compliance Monitoring                 |
| 452       | MCAE3    | Risk Assessment                       |
| 453       | MCAE4    | Policy Development                    |
| 454       | MCAE5    | Training and Education                |
| 455       | MCAE6    | Internal Auditing                     |
| 456       | MCAE7    | Compliance Reporting                  |
| 457       | MCAE8    | Data Privacy and Security             |
| 458       | MCAE9    | Conflict of Interest Management       |
| 459       | MCAE10   | Assurance and Quality Control         |
| 460       | MCAE11   | Stakeholder Engagement                |
| 461       | MCAE12   | Documentation and Recordkeeping       |
| 462       | MCAE13   | Crisis Management                     |
| 463       | MCAE14   | Cross-functional Collaboration        |
| 464       | MCAE15   | Professional Development              |
| 466       | FE1      | Trend Identification                  |
| 467       | FE2      | Market Research                       |
| 468       | FE3      | Risk Assessment                       |
| 469       | FE4      | Financial Modeling                    |
| 470       | FE5      | Valuation Analysis                    |
| 471       | FE6      | Cost Analysis                         |
| 472       | FE7      | Investment Analysis                   |
| 473       | FE8      | Mergers and Acquisitions (M&A)        |
| 474       | FE9      | Capital Structure Analysis            |
| 475       | FE10     | Economic Impact Analysis              |
| 476       | FE11     | Data Visualisation                    |
| 477       | FE12     | Stakeholder Communication             |
| 478       | FE13     | Economic Policy Analysis              |
| 479       | FE14     | Continuous Learning                   |

### Step 4 - Run the automate data addition to that week

Run the following command to automate the data addition for the week:

```bash
python automate_week.py
```

Resepectively input your email and password when prompted. For the Start date, input `2025-07-07` or the start date of the week you are working on.
Thereshould be a day_records_2025-07-07.csv file in the same directory as the script. (Like wise create a new CSV file for each week you want to add data for)
