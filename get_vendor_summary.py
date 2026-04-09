import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest_file
import os



def create_vendor_summary(conn):
    vendor_sales_summary = pd.read_sql("""WITH FreightSummary as (select vendornumber,sum(freight) as freightcost 
    from vendor_invoice 
    group by vendornumber),
    
    PurchaseSummary as ( select
        p.vendorname,
        p.vendornumber,
        p.brand,
        p.description,
        p.purchaseprice,
        pp.volume,
        pp.price as ActualPrice,
        sum(p.quantity) as TotalPurchaseQuantity,
        sum(p.Dollars) as TotalPurchaseDollars
        from purchases as p
        inner join purchase_prices as pp
        on p.brand = pp.brand
        where p.purchaseprice > 0 
        group by p.vendorname,
        p.vendornumber,
        p.brand ),
    
    SalesSummary as ( select 
    vendorno,
    brand,
    sum(salesdollars) as TotalSalesDollars,
    sum(salesprice) as TotalSalesPrice,
    sum(salesquantity) as TotalSalesQuantity,
    sum(exciseTax) as TotalSalesTax
    from sales
    group by Vendorno,brand )
    
    select ps.vendornumber,
    ps.description,
    ps.vendorname,
    ps.brand,
    ps.purchaseprice,
    ps.actualprice,
    ps.volume,
    ps.totalpurchasequantity,
    ps.totalpurchasedollars,
    ss.totalsalesquantity,
    ss.totalsalesdollars,
    ss.totalsalesprice,
    ss.totalsalestax,
    fs.freightcost
    from PurchaseSummary ps
    left join SalesSummary ss
    on ps.vendornumber = ss.vendorno
    and ps.brand = ss.brand
    left join FreightSummary fs
    on ps.vendornumber = fs.vendornumber
    order by ps.totalpurchasedollars desc""" ,conn)

    return vendor_sales_summary

def clean_data(vendor_sales_summary):
    #Changing datatype to float
    vendor_sales_summary["volume"] = vendor_sales_summary["volume"].astype('float64')

    # filling mising values with 0
    vendor_sales_summary.fillna(0,inplace = True)

    #removing spaces from categorical columns
    vendor_sales_summary["vendorname"] = vendor_sales_summary["vendorname"].str.strip()

    #creating new columns for better analysis
    vendor_sales_summary["GrossProfit"] = vendor_sales_summary["TotalSalesDollars"] - vendor_sales_summary["TotalPurchaseDollars"]
    vendor_sales_summary["ProfitMargin"] = (vendor_sales_summary["GrossProfit"] / vendor_sales_summary["TotalSalesDollars"] )*100  
    vendor_sales_summary["StockTurnover"]  = vendor_sales_summary["TotalSalesQuantity"] /  vendor_sales_summary["TotalPurchaseQuantity"]
    vendor_sales_summary["SalestoPurchaseRatio"]  = vendor_sales_summary["TotalSalesDollars"] / vendor_sales_summary["TotalPurchaseDollars"] 
  
    return vendor_sales_summary




log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "ingest_vendor_summary.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def ingest_vendor_summary(df):
    try:
        logging.info("Starting ingestion for vendor_sales_summary")
        logging.info(f"Rows to insert: {len(df)}")

        conn = sqlite3.connect("inventory.db")

        df.to_sql(
            "vendor_sales_summary",
            conn,
            if_exists="replace",
            index=False
        )

        logging.info("Ingestion completed successfully")

        conn.close()

    except Exception as e:
        logging.error(f"Ingestion failed: {e}")
        raise
    