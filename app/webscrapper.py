from bs4 import BeautifulSoup as bs
import urllib.request as request
import re
from datetime import datetime as dt
import csv


# create file with column headers

header = ['Loan Term', 'Loan Amount', 'Loan Provider', 'Loan Product', 'Average APR', 'Source', 'Date Extracted']
with open('historical_average_apr.csv', 'w', newline='') as f:
    csv_writer = csv.DictWriter(f, fieldnames=header)
    csv_writer.writeheader()


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
                    date_extracted = dt.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    for c_match in company_matches:
                        for p_match in product_matches:
                            for r_match in rep_apr_matches:
                                rate = str(r_match).replace('"RepresentativeAPR":', '')
                                product = str(p_match).replace(',', ' -')
                                source = 'Moneyfacts'
                                f.writelines(f'{loan_term}, {loan_amount}, {c_match}'
                                             f', {product}, {rate}, {source}, {date_extracted}'+"\n")
                                # print(f'{loan_term}, {loan_amount}, {c_match}, {product},{rate}, {source}'
                                #       f',{date_extracted}')

                a += 2
                b += 2
            else:
                break
        loan_amount += 1000


while loan_term < 61:
    loan_inc()
    loan_term += 12
