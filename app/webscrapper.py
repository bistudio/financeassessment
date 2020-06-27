from bs4 import BeautifulSoup as bs
import urllib.request as request
import lxml
import re
from datetime import datetime as dt
import csv


loan_term = 12


def loan_inc():
    loan_amount = 1000
    while loan_amount < 31000:
        url = f"https://moneyfacts.co.uk/loans/personal-loans/?id=null&loan-amount={loan_amount}&repayment-term-in-months={loan_term}&for-existing-customers-only=2&fees-and-charges=null&speed-of-decision-and-funds=null&age=21&credit-rating=null&guarantor-accepted=2&features=null"
        sauce = request.urlopen(url).read()
        soup = bs(sauce, 'lxml')
        soup.prettify()

        # search items in string Company, LoanName, RepresentativeAPR

        script_tag = soup.find_all('script', attrs={'data-id': "personal-loans-finder"})
        html_string = str(script_tag)
        a_string = html_string
        substring = 'Company'
        matches = re.finditer(substring, a_string)
        matches_position = [match.start() for match in matches]
        a = 0
        b = 1
        j = 0
        for i in matches_position:
            if b < len(matches_position):
                with open('historical_average_apr.csv', 'a') as f:
                    search_string = html_string[matches_position[a]:matches_position[b]]
                    company_pattern = re.compile(r'^Company":\"(.+?)\"')
                    company_matches = re.findall(company_pattern, search_string)
                    product_pattern = re.compile(r'"LoanName":\"(.+?)\"')
                    product_matches = re.findall(product_pattern, search_string)
                    rep_apr_pattern = re.compile(r'"RepresentativeAPR":\d*\d*\.\d*\d*')
                    rep_apr_matches = re.findall(rep_apr_pattern, search_string)
                    header = ['Loan Term', 'Loan Amount', 'Loan Provider', 'Loan Product', 'Representative APR', 'Date Extracted']
                    date_extracted = dt.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    for c_match in company_matches:
                        for p_match in product_matches:
                            for r_match in rep_apr_matches:
                                f.writelines(f'{loan_term}, {loan_amount}, "{c_match}", "{p_match}", {r_match}, {date_extracted}'+"\n")
                                # print(f'{loan_term}, {loan_amount}, "{c_match}", "{p_match}",{r_match}'
                                #       f',{date_extracted}')
                a += 2
                b += 2
            else:
                break
        loan_amount += 1000


while loan_term < 61:
    loan_inc()
    loan_term += 12


#  Loan Amount Loan Term  "Company":'AA', "loanName":'Member', "RepresentativeAPR":14.3  Date Extrated from Moneyfact


# Company":(["'])(?:(?=(\\?))\2.)*?\1
# "LoanName":(["'])(?:(?=(\\?))\2.)*?\1
# "RepresentativeAPR":\d*\d*\.\d*\d*