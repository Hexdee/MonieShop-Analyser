#!/usr/bin/env python3

from os import listdir, path
import datetime
from calendar import month_name

"""
Monieshop Analytics software

Problem statement:

Monieshop is a supermarket that sells different products to its customers. It uses a digital 
accounting system to track its sales transactions. The digital accounting system uses text files 
to store transaction data. Here is a brief description of the file format:

Each text file contains the transaction data for 1 day.
A single line in a transaction file stores information related to 1 transaction in a comma-separated format.
The information present is:
- salesStaffId
- transaction time
- The products sold. (format "[productId1:quantity|productId2:quantity]")
- sale amount

Example for a line in a transaction file:
"4,2025-01-01T16:58:53,[726107:5|553776:5],2114.235"

You're asked to write analytics software that reads through 2024 transactions' files and reports 
the following metrics:
- Highest sales volume in a day
- Highest sales value in a day  
- Most sold product ID by volume
- Highest sales staff ID for each month
- Highest hour of the day by average transaction volume
"""

"""
TODO:
- [x] Read in all the transactions
    - [x] Parse the transactions
    - [x] Keep track of some metrics
    - [x] Metrics to track: daily volume, daily value, product volume, monthly staff sales, hourly volumes
- [x] Print out the metrics max values as needed
- [] Sort monthly staff sales by month
"""


# Create the sales object
class Sale:
    def __init__(self, record):
        self.staff = record[0]
        self.timestamp = self.format_timestamp(record[1])
        self.products = self.format_products(record[2])
        self.amount = record[3]

    def format_products(self, products):
        products = products[1:-1].split('|')
        formatted_products = []
        for product in products:
            product_id, quantity = product.split(':')
            formatted_products.append({'id': product_id, 'quantity': quantity})
        return formatted_products

    def format_timestamp(self, timestamp):
        return datetime.datetime.fromisoformat(timestamp)
    
    def __str__(self):
        return f"Staff ID: {self.staff}, Timestamp: {self.timestamp}, Products: {self.products}, Amount: {self.amount}"


class MonieshopAnalyser:
    def __init__(self, folder_path):
        self.transactions = []
        self.folder_path = folder_path
        self.daily_volume = dict()
        self.daily_value = dict()
        self.product_volume = dict()
        self.monthly_staff_sales = dict()
        self.hourly_volumes = dict()

    def analyse_yearly_transactions(self, folder_path=None):
        folder_path = folder_path if folder_path else self.folder_path
        if folder_path is None:
            raise ValueError("folder_path is required to analyse yearly transactions!")
        # Read in all the transactions while parsing each sale transaction and keeping track of daily volume, daily value, product volume, monthly staff sales, hourly volumes
        self.get_transactions()

        # Print out the metrics max values as needed
        self.print_metrics()      
    
    def get_transactions(self):
        """
        Read in all the transactions while:
            - Parsing each sale transaction
            - and keeping track of daily volume, daily value, product volume, monthly staff sales, hourly volumes
        """
        transactions = []
        for filename in listdir(self.folder_path):
            with open(path.join(self.folder_path, filename)) as f:
                for line in f:
                    # Parse the sale transaction
                    sale = Sale(line.strip().split(','))
                    # Keep track of metrics
                    self.update_metrics(sale)
                    transactions.append(sale)
        self.transactions = transactions


    def update_metrics(self, sale: Sale):
        """
        Update metrics for the given sale
        """
        # Get date components
        date = sale.timestamp.date()
        month = sale.timestamp.strftime('%Y-%m')
        hour = sale.timestamp.hour

        # Calculate total volume for this sale
        sale_volume = sum(int(product['quantity']) for product in sale.products)

        # Update daily metrics setting default values for new dates
        self.daily_volume[date] = self.daily_volume.get(date, 0) + sale_volume
        self.daily_value[date] = self.daily_value.get(date, 0) + float(sale.amount)

        # Update product volumes
        for product in sale.products:
            self.product_volume[product['id']] = self.product_volume.get(product['id'], 0) + int(product['quantity'])

        # Update monthly staff sales
        self.monthly_staff_sales[month] = self.monthly_staff_sales.get(month, dict())
        self.monthly_staff_sales[month][sale.staff] = self.monthly_staff_sales[month].get(sale.staff, 0) + sale_volume

        # Update hourly volumes
        if hour not in self.hourly_volumes:
            self.hourly_volumes[hour] = []
        self.hourly_volumes[hour].append(sale_volume)

    def print_metrics(self):
        """
        Print out the metrics max values as needed
        """
        # Calculate results
        highest_volume_day = max(self.daily_volume.items(), key=lambda x: x[1])
        highest_value_day = max(self.daily_value.items(), key=lambda x: x[1])
        most_sold_product = max(self.product_volume.items(), key=lambda x: x[1])
        # Calculate top staff per month
        monthly_top_staff = dict()
        for month, staff in self.monthly_staff_sales.items():
            monthly_top_staff[month] = max(staff.items(), key=lambda x: x[1])
        # Calculate average hourly volume
        avg_hourly_volume = dict()
        for hour, volumes in self.hourly_volumes.items():
            avg_hourly_volume[hour] = sum(volumes)/len(volumes)
        peak_hour = max(avg_hourly_volume.items(), key=lambda x: x[1])

        # Print results
        print(f"1. Highest sales volume in a day: {highest_volume_day[1]} units on {highest_volume_day[0]}")
        print(f"2. Highest sales value in a day: ${highest_value_day[1]:.2f} on {highest_value_day[0]}")
        print(f"3. Most sold product ID: {most_sold_product[0]} with {most_sold_product[1]} units")
        print("4. Highest sales staff ID for each month:")
        
        for month, staff in sorted(monthly_top_staff.items(), key=lambda x: x[0]):
            month = month_name[int(month[-2:])]
            print(f"    {month}: Staff ID {staff[0]} with ${staff[1]:.2f} sales")
        print(f"5. Peak hour by average transaction volume: {peak_hour[0]}:00-{peak_hour[0]}:59 with an average transaction volume of {peak_hour[1]:.2f}")


if __name__ == "__main__":
    print("Test Case 1:")
    instance1 = MonieshopAnalyser("sample-data/test-case-1")
    instance1.analyse_yearly_transactions()
    print("\n", "=" * 80, "\n")
    print("Test Case 2:")
    instance2 = MonieshopAnalyser("sample-data/test-case-2")
    instance2.analyse_yearly_transactions()
    print("\n", "=" * 80, "\n")
    print("Test Case 3:")
    instance3 = MonieshopAnalyser("sample-data/test-case-3")
    instance3.analyse_yearly_transactions()
    print("\n", "=" * 80, "\n")
    print("Test Case 4:")
    instance4 = MonieshopAnalyser("sample-data/test-case-4")
    instance4.analyse_yearly_transactions()
    print("\n", "=" * 80, "\n")
    print("Test Case 5:")
    instance5 = MonieshopAnalyser("sample-data/test-case-5")
    instance5.analyse_yearly_transactions()
