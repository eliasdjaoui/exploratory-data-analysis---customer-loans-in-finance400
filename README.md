# exploratory-data-analysis---customer-loans-in-finance

Table of Contents, if the README file is long
A description of the project: what it does, the aim of the project, and what you learned
Installation instructions
Usage instructions
File structure of the project
License information


### Loan Data Dictionary

| **Field**                     | **Description**                                                                                                                                      | **Type**    |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| `id`                           | Unique ID of the loan                                                                                                                                | `string`    |
| `member_id`                    | ID of the member who took out the loan                                                                                                               | `string`    |
| `loan_amount`                  | Amount of loan the applicant received                                                                                                                | `float`     |
| `funded_amount`                | The total amount committed to the loan at that point in time                                                                                         | `float`     |
| `funded_amount_inv`            | The total amount committed by investors for that loan at that point in time                                                                          | `float`     |
| `term`                         | The number of monthly payments for the loan                                                                                                          | `integer`   |
| `int_rate (APR)`               | Annual (APR) interest rate of the loan                                                                                                               | `float`     |
| `instalment`                   | The monthly payment owed by the borrower, inclusive of interest                                                                                      | `float`     |
| `grade`                        | Loan company (LC) assigned loan grade                                                                                                                | `string`    |
| `sub_grade`                    | LC assigned loan sub grade                                                                                                                           | `string`    |
| `employment_length`            | Employment length in years                                                                                                                           | `integer`   |
| `home_ownership`               | The home ownership status provided by the borrower                                                                                                   | `string`    |
| `annual_inc`                   | The annual income of the borrower                                                                                                                    | `float`     |
| `verification_status`          | Indicates whether the borrower's income was verified by the LC or the income source was verified                                                     | `string`    |
| `issue_date`                   | Issue date of the loan                                                                                                                               | `date`      |
| `loan_status`                  | Current status of the loan                                                                                                                           | `string`    |
| `payment_plan`                 | Indicates if a payment plan is in place for the loan (indicating the borrower is struggling to pay)                                                  | `string`    |
| `purpose`                      | A category provided by the borrower for the loan request                                                                                             | `string`    |
| `dti`                          | Debt-to-income ratio: calculated using the borrower's total monthly debt payments on the total debt obligations, excluding mortgage and the LC loan, divided by the borrower’s self-reported monthly income | `float`     |
| `delinq_2yr`                   | The number of 30+ days past-due payments in the borrower's credit file for the past 2 years                                                           | `integer`   |
| `earliest_credit_line`         | The month the borrower's earliest reported credit line was opened                                                                                    | `date`      |
| `inq_last_6mths`               | The number of inquiries in the past 6 months (excluding auto and mortgage inquiries)                                                                 | `integer`   |
| `mths_since_last_record`       | The number of months since the last public record                                                                                                    | `integer`   |
| `open_accounts`                | The number of open credit lines in the borrower's credit file                                                                                        | `integer`   |
| `total_accounts`               | The total number of credit lines currently in the borrower's credit file                                                                             | `integer`   |
| `out_prncp`                    | Remaining outstanding principal for the total amount funded                                                                                          | `float`     |
| `out_prncp_inv`                | Remaining outstanding principal for the portion of the total amount funded by investors                                                              | `float`     |
| `total_payment`                | Payments received to date for the total amount funded                                                                                                | `float`     |
| `total_rec_int`                | Interest received to date                                                                                                                            | `float`     |
| `total_rec_late_fee`           | Late fees received to date                                                                                                                           | `float`     |
| `recoveries`                   | Post charge-off gross recovery                                                                                                                      | `float`     |
| `collection_recovery_fee`      | Post charge-off collection fee                                                                                                                       | `float`     |
| `last_payment_date`            | Date on which last payment was received                                                                                                              | `date`      |
| `last_payment_amount`          | Last total payment amount received                                                                                                                   | `float`     |
| `next_payment_date`            | Next scheduled payment date                                                                                                                          | `date`      |
| `last_credit_pull_date`        | The most recent month LC pulled credit for this loan                                                                                                 | `date`      |
| `collections_12_mths_ex_med`   | Number of collections in the past 12 months, excluding medical collections                                                                           | `integer`   |
| `mths_since_last_major_derog`  | Months since most recent 90-day or worse rating                                                                                                      | `integer`   |
| `policy_code`                  | Publicly available policy code: `1` for new products, `2` for products not publicly available                                                        | `integer`   |
| `application_type`             | Indicates whether the loan is an individual application or a joint application with two co-borrowers                                                 | `string`    |


