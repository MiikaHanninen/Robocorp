from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
pdf = PDF()


@task
def order_robots_from_RobotSpareBin():
    """Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images."""
    browser.configure(
        slowmo=100,)
    open_robot_order_website()
    close_annoying_modal()
    orders = get_orders()
    process_orders(orders)




    
    
def open_robot_order_website():
    """Opens up the order web site"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order/")

def get_orders():
    http = HTTP()
    url = "https://robotsparebinindustries.com/orders.csv"
    filename = "orders.csv"
    http.download(url, filename, overwrite=True)
    tables = Tables()

    orders_table = tables.read_table_from_csv(filename)

    return orders_table

def process_orders(orders):
    for row in orders:
        fill_the_form(row)


def close_annoying_modal():
    page = browser.page()
    page.click("text=Ok")

def fill_the_form(row):
    page = browser.page()
    order_number = row['Order number']
    print(f"order number: {order_number}")

    body_value = row["Body"] 
    # Täytä 'Order number'
    page.select_option('select[name="head"]', row['Head'])
    page.click(f'input[name="body"][value="{body_value}"]')
    page.fill('input[placeholder="Enter the part number for the legs"]' , str(row['Legs']))


    page.fill('input[name="address"]', row['Address'])

    # Klikkaa tilaus-nappia
    page.click('button[id="preview"]')
    while True:
        page.click('button[id="order"]')
        page.wait_for_timeout(2000)

        if page.is_visible('text=Thank you for your order!'): 
            break

    page.click('button[id="order-another"]')
    close_annoying_modal()


