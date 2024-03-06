from os import name
import re
from io import StringIO
import PyPDF2
import pandas as pd


def get_sem7_data(df: pd.DataFrame, sem7_final: str):
    # Extract Total Credit
    total_credit_match = re.search(r"Total Credit : (\d+\.\d+)", sem7_final)
    total_credit = total_credit_match.group(1) if total_credit_match else ""

    # Extract EGP
    egp_match = re.search(r"EGP : (\d+\.\d+)", sem7_final)
    egp = egp_match.group(1) if egp_match else ""

    # Extract SGPA
    sgpa_match = re.search(r"SGPA : (\d+\.\d+)", sem7_final)
    sgpa = sgpa_match.group(1) if sgpa_match else ""

    # Define a list of subject codes
    subject_codes = [
        "197044701",
        "197044702",
        "197044703",
        "197044704",
        "197044705",
        "197044706",
        "197044707",
        "197044708",
    ]

    # Initialize an empty dictionary to store the data
    data = {}

    # Iterate over the subject codes
    for code in subject_codes:
        # Initialize empty dictionaries for each subject
        subject_data = {
            "ESE": "",
            "ISE": "",
            "ICA": "",
            "POE": "",
            "Total": "",
            "Sts": "",
        }

        # Check if the subject code exists in the dataframe
        if len(df[df["CODE"] == code]) > 0:
            # Get the data for each column
            subject_data["ESE"] = df[df["CODE"] == code].iloc[0, 3]
            subject_data["ISE"] = df[df["CODE"] == code].iloc[0, 7]
            subject_data["ICA"] = (
                df[df["CODE"] == code].iloc[0, 17]
                if code not in ["197044704", "197044708"]
                else df[df["CODE"] == code].iloc[0, 5]
            )
            subject_data["POE"] = df[df["CODE"] == code].iloc[0, 21]
            subject_data["Total"] = df[df["CODE"] == code].iloc[0, 27]
            subject_data["Sts"] = df[df["CODE"] == code].iloc[0, 31]

        # Add the subject data to the main data dictionary
        data[code] = subject_data

    # Add the total credit, EGP, and SGPA to the data dictionary
    data["Total_Credit"] = total_credit
    data["EGP"] = egp
    data["SGPA"] = sgpa
    # print("data: ", data)
    return data


def get_sem8_data(df: pd.DataFrame, sem8_final: str):
    # Extract Total Credit
    total_credit_match = re.search(r"Total Credit : (\w+\.?\w+)", sem8_final)
    total_credit = total_credit_match.group(1) if total_credit_match else ""
    # Extract EGP
    egp_match = re.search(r"EGP : (\w+\.?\w+)", sem8_final)
    egp = egp_match.group(1) if egp_match else ""
    # Extract SGPA
    sgpa_match = re.search(r"SGPA : (\w+\.?\w+)", sem8_final)
    sgpa = sgpa_match.group(1) if sgpa_match else ""
    # Define a list of subject codes
    subject_codes = [
        "197044801",
        "197044802",
        "197044803",
        "197044804",
        "197044805",
        "197044806",
        "197044807",
    ]
    # Initialize an empty dictionary to store the data
    data = {}
    # Iterate over the subject codes
    for code in subject_codes:
        # Initialize empty dictionaries for each subject
        subject_data = {
            "ESE": "",
            "ISE": "",
            "ICA": "",
            "POE": "",
            "Total": "",
            "Sts": "",
        }

        # Check if the subject code exists in the dataframe
        if len(df[df["CODE"] == code]) > 0:
            # Get the data for each column
            subject_data["ESE"] = df[df["CODE"] == code].iloc[0, 3]
            subject_data["ISE"] = df[df["CODE"] == code].iloc[0, 7]
            subject_data["ICA"] = (
                df[df["CODE"] == code].iloc[0, 17]
                if code not in ["197044804", "197044805", "197044806", "197044807"]
                else df[df["CODE"] == code].iloc[0, 5]
            )
            subject_data["POE"] = df[df["CODE"] == code].iloc[0, 21]
            subject_data["Total"] = df[df["CODE"] == code].iloc[0, 27]
            subject_data["Sts"] = df[df["CODE"] == code].iloc[0, 31]

        # Add the subject data to the main data dictionary
        data[code] = subject_data
    # Add the total credit, EGP, and SGPA to the data dictionary
    data["Total_Credit"] = total_credit
    data["EGP"] = egp
    data["SGPA"] = sgpa

    return data


def handle_single_page(text):
    # print("text: \n", text)
    table = text.split("\n")
    # print("table: \n", table[3])

    sem7_table = []
    sem7_table += [table[x] for x in range(5, 13)]
    # Split the first element to get column names
    columns = sem7_table[0].split()
    # Create the DataFrame
    sem7_df = pd.DataFrame([x.split() for x in sem7_table[1:]], columns=columns)

    sem7_data = get_sem7_data(sem7_df, table[13])

    sem8_table = []
    sem8_table += [table[x] for x in range(15, 21)]
    # Split the first element to get column names
    columns = sem8_table[0].split()
    # Create the DataFrame
    sem8_df = pd.DataFrame([x.split() for x in sem8_table[1:]], columns=columns)
    sem8_data = get_sem8_data(sem8_df, table[21])

    # print("sem7_data: ", sem7_data)
    # print("sem8_data: ", sem8_data)

    seat_no_pattern = re.compile(r"Seat\s*No\s*:\s*(\*?\w+)")
    prn_no_pattern = re.compile(r"Prn\s*No.-\s*(\d+)")
    name_pattern = re.compile(r"NAME:\s*(.+)")
    seat_no_match = seat_no_pattern.search(table[2] + table[1] + table[3])
    prn_no_match = prn_no_pattern.search(table[2] + table[1] + table[3])
    name_match = name_pattern.search(table[3] + table[4] + table[2])
    seat_no = seat_no_match.group(1) if seat_no_match else ""
    prn_no = prn_no_match.group(1) if prn_no_match else ""
    name = name_match.group(1) if name_match else ""

    # print("seat_no: ", seat_no)
    # print("prn_no: ", prn_no)
    # print("name: ", name)

    percentage_pattern = re.compile(r"Percentage:(\w+\.?\w+)")
    status_pattern = re.compile(r"GPA/SGPA:\s*(\w+\.?\w+)\s*\|\s*Status:\s*(\w+)")
    percentage_match = percentage_pattern.search(table[26] + table[27] + table[25])
    status_match = status_pattern.search(
        table[26] + table[27] + table[28] if len(table) > 28 else table[27] + table[26]
    )
    percentage = percentage_match.group(1) if percentage_match else ""
    overall_status = status_match.group(2) if status_match else ""

    # print("percentage: ", percentage)
    # print("overall_status: ", overall_status)

    return {
        "Exam_Seat_No": seat_no,
        "PRN_No": prn_no,
        "Name": name,
        "Sem7": sem7_data,
        "Sem8": sem8_data,
        "Status": overall_status,
        "Percentage": percentage,
    }


def extract_data_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        data_list = []
        # for page_num in range(2, 10):
        for page_num in range(2, len(reader.pages) - 1):
            single_page = reader.pages[page_num].extract_text()
            data = handle_single_page(single_page)
            data_list.append(data)
        return data_list


pdf_path = "b_tech_sem_VII_VIII_revised_19022024.pdf"
data_list = extract_data_from_pdf(pdf_path)

# print("data_list: \n", data_list)


html_head = """
<thead>
    <tr>
        <td rowspan="3">Exam Seat No.</td>
        <td rowspan="3">PRN No.</td>
        <td rowspan="3">Name of Student</td>
        <td colspan="51">Sem 3</td>
        <td colspan="45">Sem 4</td>
        <td rowspan="3">Status</td>
        <td rowspan="3">Percentage</td>
    </tr>
    <tr>
        <td colspan="6">197044701</td>
        <td colspan="6">197044702</td>
        <td colspan="6">197044703</td>
        <td colspan="6">197044704</td>
        <td colspan="6">197044705</td>
        <td colspan="6">197044706</td>
        <td colspan="6">197044707</td>
        <td colspan="6">197044708</td>
        <td rowspan="2">Total Credit</td>
        <td rowspan="2">EGP</td>
        <td rowspan="2">SGPA</td>
        <td colspan="6">197044801</td>
        <td colspan="6">197044802</td>
        <td colspan="6">197044803</td>
        <td colspan="6">197044804</td>
        <td colspan="6">197044805</td>
        <td colspan="6">197044806</td>
        <td colspan="6">197044807</td>
        <td rowspan="2">Total Credit</td>
        <td rowspan="2">EGP</td>
        <td rowspan="2">SGPA</td>
    </tr>
    <tr>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
        <td>ESE</td>
        <td>ISE</td>
        <td>ICA</td>
        <td>POE</td>
        <td>Total</td>
        <td>Sts</td>
    </tr>
</thead>
"""

all_data = ""
for student in data_list:
    one_row = ""
    one_row += f"<td>{student['Exam_Seat_No']}</td>"
    one_row += f"<td>{student['PRN_No']}</td>"
    one_row += f"<td>{student['Name']}</td>"

    for i in ["Sem7", "Sem8"]:
        for data in student[i]:
            # Check if the value is a dictionary before iterating over it
            if isinstance(student[i][data], dict):
                for abb in student[i][data]:
                    one_row += f"<td>{student[i][data][abb]}</td>"
            else:
                one_row += f"<td>{student[i][data]}</td>"

    one_row += f"<td>{student['Status']}</td>"
    one_row += f"<td>{student['Percentage']}</td>"
    all_data += f"<tr>{one_row}</tr>"


table = f"<table>{html_head}<tbody>{all_data}</tbody></table>"
result = pd.read_html(StringIO(table))
result[0].to_excel("sem7_8_revised.xlsx")
