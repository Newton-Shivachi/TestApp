import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

sales_data_layers = pd.read_csv("saleslayers.csv") if "saleslayers.csv" in os.listdir() else pd.DataFrame(columns=['Date', 'Product', 'Sales', 'Quantity', 'Payment Mode'])
inventory_data_layers = pd.read_csv("inventorylayers.csv") if "inventorylayers.csv" in os.listdir() else pd.DataFrame(columns=['Date', 'Product', 'Quantity'])
expense_data_layers = pd.read_csv("expenselayers.csv") if "expenselayers.csv" in os.listdir() else pd.DataFrame(columns=['Date', 'Expense', 'Bill'])
egg_production=pd.read_csv("eggproduction.csv") if "eggproduction.csv" in os.listdir() else pd.DataFrame(columns=['Date','Laying Birds','number of Eggs'])

sales_data_meat = pd.read_csv("salesmeat.csv") if "salesmeat.csv" in os.listdir() else pd.DataFrame(columns=['Date', 'Product', 'Sales', 'Quantity', 'Payment Mode'])
inventory_data_meat = pd.read_csv("inventorymeat.csv") if "inventorymeat.csv" in os.listdir() else pd.DataFrame(columns=['Date','Week','Expense','Cost','Market Price','Number of Chicks','Group'])
expense_data_meat = pd.read_csv("expensemeat.csv") if "expensemeat.csv" in os.listdir() else pd.DataFrame(columns=['Date', 'Expense', 'Bill'])

##function to add layers Expenses
def add_expense_layers(date, expense, bill):
    global expense_data_layers
    new_expense_layers=pd.DataFrame({'Date':[date],'Expense':[expense],'Bill':[bill]})
    expense_data_layers=pd.concat([expense_data_layers,new_expense_layers],ignore_index=True)

def add_egg_production(date, birds, eggs):
    global egg_production
    new_egg_entry=pd.DataFrame({'Date':[date],'Laying Birds':[birds],'number of Eggs':[eggs]})
    egg_production = pd.concat([egg_production, new_egg_entry], ignore_index=True)

##function to add meat Expenses
def add_expense_meat(date, expense, bill):
    global expense_data_meat
    new_expense_meat=pd.DataFrame({'Date':[date],'Expense':[expense],'Bill':[bill]})
    expense_data_meat=pd.concat([expense_data_meat,new_expense_meat],ignore_index=True)
    
def add_expense_chick(date,week, expense, cost, market_price,number_chicks,group):
    global inventory_data_meat
    new_inventory_meat=pd.DataFrame({'Date':[date],'Week':[week],'Expense':[expense],'Cost':[cost],'Market Price':[market_price],'Number of Chicks':[number_chicks],'Group':[group]})
    inventory_data_meat=pd.concat([inventory_data_meat,new_inventory_meat],ignore_index=True)

# Function to add or update layers inventory data
def add_or_update_inventory_layers(date, product, quantity):
    global inventory_data_layers
    if product in inventory_data_layers['Product'].values:
        # Update existing product quantity
        inventory_data_layers.loc[inventory_data_layers['Product'] == product, 'Quantity'] += quantity
    else:
        # Add new product to inventory
        new_entry_layers = pd.DataFrame({'Date': [date], 'Product': [product], 'Quantity': [quantity]})
        inventory_data_layers = pd.concat([inventory_data_layers, new_entry_layers], ignore_index=True)
        
# Function to subtract sold quantity from Layers inventory
def update_inventory_layers_on_sale(product, quantity_sold):
    global inventory_data_layers
    if product in inventory_data_layers['Product'].values:
        # Subtract sold quantity from inventory
        inventory_data_layers.loc[inventory_data_layers['Product'] == product, 'Quantity'] -= quantity_sold
        if inventory_data_layers.loc[inventory_data_layers['Product'] == product, 'Quantity'].values[0] == 0:
            st.warning(f"No more {product} available in inventory!")
    else:
        st.warning(f"No {product} found in inventory!")

        
# Function to add a layers sales entry to the DataFrame
def add_sales_layers_entry(date, product, sales, quantities, payment_mode):
    global sales_data_layers
    add_or_update_inventory_layers(date, product, -sum(quantities))  # Subtract sold quantities from inventory
    
    # Iterate over each sales value and quantity and add a separate entry to the sales data
    for sales_value, quantity in zip(sales, quantities):
        new_entry = pd.DataFrame({'Date': [date], 'Product': [product], 'Sales': [sales_value], 'Quantity': [quantity], 'Payment Mode': [payment_mode]})
        sales_data_layers = pd.concat([sales_data_layers, new_entry], ignore_index=True)
        
# Function to add a meat sales entry to the DataFrame
def add_sales_meat_entry(date, product, sales, quantities, payment_mode):
    global sales_data_meat
    # Iterate over each sales value and quantity and add a separate entry to the sales data
    new_entry_meat = pd.DataFrame({'Date': [date], 'Product': [product], 'Sales': [sales], 'Quantity': [quantities], 'Payment Mode': [payment_mode]})
    sales_data_meat = pd.concat([sales_data_meat, new_entry_meat], ignore_index=True)
        
# Function to display the sales data in a DataFrame
def display_sales_data_layers():
    st.write(sales_data_layers)
# Function to display the sales data in a DataFrame
def display_sales_data_meat():
    st.write(sales_data_meat)

# Function to display the inventory data in a DataFrame
def display_inventory_data_layers():
    st.write(inventory_data_layers)
# Function to display the inventory data in a DataFrame
def display_inventory_data_meat():
    st.write(inventory_data_meat)
    
def display_egg_production():
    st.write(egg_production)
    
# Funtion to display the expense data in a data frame
def display_expense_data_layers():
    st.write(expense_data_layers)
# Funtion to display the expense data in a data frame
def display_expense_data_meat():
    st.write(expense_data_meat)

st.title("MATURE BIRDS SECTION")
layers_action = st.radio("Select action", ["Rocord ", "Mature Birds Analysis"])
if layers_action =="Mature Birds Analysis":
    st.title("Business Analytics :bar_chart:")
    egg_production["Date"]=pd.to_datetime(egg_production["Date"])
    start_date= egg_production["Date"].min()
    end_date= egg_production["Date"].max()
    col1,col2=st.columns((2))
    with col1:
        date1=pd.to_datetime(st.date_input("Startdate", start_date)) 
    with col2:
        date2=pd.to_datetime(st.date_input("Enddate",end_date)) 
    egg_production_data=egg_production[(egg_production["Date"]>=date1)&(egg_production["Date"]<=date2)].copy()
    egg_production_data['Missed laying']=egg_production_data['Laying Birds']-egg_production_data['number of Eggs']
    egg_line_graph=px.line(egg_production_data,x='Date',y=['Laying Birds','number of Eggs','Missed laying'],height=500, width=1000,template='gridon')
    st.plotly_chart(egg_line_graph,use_container_width=True)
    egg_production_data['Date']=pd.to_datetime(egg_production_data['Date'])
    egg_production_data['Months']=egg_production_data['Date'].dt.month
    egg_bar_graph=px.bar(egg_production_data,x='Months',y=['number of Eggs','Missed laying'],height=500, width=1000,template='gridon')
    st.plotly_chart(egg_bar_graph,use_container_width=True)
    egg_data_monthly=egg_production_data.groupby('Months')['number of Eggs'].sum().reset_index()
    missed_egg_data_monthly=egg_production_data.groupby('Months')['Missed laying'].sum().reset_index()
    col22,col33=st.columns((2))
    with col22:
        with st.expander('View monthwise total layed eggs'):
            st.write(egg_data_monthly)
    with col33:
        with st.expander('View monthwise total layers that did not lay'):
            st.write(missed_egg_data_monthly)
    st.header('Sales analytics')
    sales_data_layers["Date"]=pd.to_datetime(sales_data_layers["Date"])
    start_date1= sales_data_layers["Date"].min()
    end_date1=sales_data_layers["Date"].max()
    col1,col2=st.columns((2))
    with col1:
        date11=pd.to_datetime(st.date_input("From", start_date1)) 
    with col2:
        date21=pd.to_datetime(st.date_input("To",end_date1)) 
    mature_sales_data=sales_data_layers[(sales_data_layers["Date"]>=date11)&(sales_data_layers["Date"]<=date21)].copy()
    filtered_mature_sales_data=st.sidebar.multiselect("Select a sold out product from mature bird",mature_sales_data["Product"].unique())
    if not filtered_mature_sales_data:
        filtered_mature_sales_data = mature_sales_data.copy()
    else:
        filtered_mature_sales_data =mature_sales_data[mature_sales_data["Product"].isin(filtered_mature_sales_data)]
    filtered_mature_sales_data["Date"]= pd.to_datetime(filtered_mature_sales_data["Date"])
    filtered_mature_sales_data["Month"]= filtered_mature_sales_data["Date"].dt.month
    filtered_mature_sales_data["Day of week"]= filtered_mature_sales_data["Date"].dt.dayofweek
    filtered_mature_sales_data["Day Of Year"]= filtered_mature_sales_data["Date"].dt.dayofyear
    filtered_mature_sales_data["Yearly Quarters"]= filtered_mature_sales_data["Date"].dt.quarter
    if st.button('Analyse your sales'):
        sales_bar_graph=px.line(filtered_mature_sales_data,x='Date',y=['Sales'],height=500, width=1000,template='gridon')
        st.plotly_chart(sales_bar_graph,use_container_width=True)
        quantity_bar_graph=px.line(filtered_mature_sales_data,x='Date',y=['Quantity'],height=500, width=1000,template='gridon')
        st.plotly_chart(quantity_bar_graph,use_container_width=True)
        sales_bar_graph1=px.bar(filtered_mature_sales_data,x='Day of week',y=['Sales'],height=500, width=1000,template='gridon')
        st.plotly_chart(sales_bar_graph1,use_container_width=True)
        quantity_bar_graph1=px.bar(filtered_mature_sales_data,x='Day of week',y=['Quantity'],height=500, width=1000,template='gridon')
        st.plotly_chart(quantity_bar_graph1,use_container_width=True)
        time_bar_graph=px.bar(filtered_mature_sales_data,x='Month',y=['Sales'],height=500, width=1000,template='gridon')
        monthwise_sales_df=filtered_mature_sales_data.groupby('Month')['Sales'].sum().reset_index()
        coll0000,col00001=st.columns((2))
        with coll0000:
            with st.expander('View the monthwise sales'):
                st.plotly_chart(time_bar_graph,use_container_width=True)
        with col00001:
            with st.expander('View monthwise Sales data frame'):
                st.write(monthwise_sales_df)
        time_bar_graphq=px.bar(filtered_mature_sales_data,x='Month',y=['Quantity'],height=500, width=1000,template='gridon')
        product_quantity_df=filtered_mature_sales_data.groupby('Product')['Quantity'].sum().reset_index()
        coll00000,col000001=st.columns((2))
        with coll00000:
            with st.expander('View the monthwise sold quantity'):
                st.plotly_chart(time_bar_graphq,use_container_width=True)
        with col000001:
            with st.expander('View monthwise quantity sold data frame'):
                st.write(product_quantity_df)
        product_bar_graph1=px.bar(filtered_mature_sales_data,x='Product',y=['Sales'],height=500, width=1000,template='gridon')
        product_sales_df=filtered_mature_sales_data.groupby('Product')['Sales'].sum().reset_index()
        coll000,col0001=st.columns((2))
        with coll000:
            with st.expander('View the monthwise product sales'):
                st.plotly_chart(product_bar_graph1,use_container_width=True)
        with col0001:
            with st.expander('View Quarterly Sales data frame'):
                st.write(product_sales_df)
        quarter_bar_graph1=px.bar(filtered_mature_sales_data,x='Yearly Quarters',y=['Sales'],height=500, width=1000,template='gridon')
        yearly_sales_df=filtered_mature_sales_data.groupby('Yearly Quarters')['Sales'].sum().reset_index()
        coll00,col001=st.columns((2))
        with coll00:
            with st.expander('View the Quarterly bar graph for Sales'):
                st.plotly_chart(quarter_bar_graph1,use_container_width=True)
        with col001:
            with st.expander('View Quarterly Sales data frame'):
                st.write(yearly_sales_df)    
        quarter_bar_graph=px.bar(filtered_mature_sales_data,x='Yearly Quarters',y=['Quantity'],height=500, width=1000,template='gridon')
        yearly_quantity_df=filtered_mature_sales_data.groupby('Yearly Quarters')['Quantity'].sum().reset_index()
        coll0,col01=st.columns((2))
        with coll0:
            with st.expander('View the Quarterly bar graph for Quantity sold'):
                st.plotly_chart(quarter_bar_graph,use_container_width=True)
        with col01:
            with st.expander('View Quarterly quantity sold data frame'):
                st.write(yearly_quantity_df)
        payment_mode = filtered_mature_sales_data.groupby('Payment Mode')['Sales'].sum().sort_values(ascending=True).reset_index()
        fig= px.pie(payment_mode,values='Sales',hole=0.5)
        fig.update_traces(text=payment_mode['Payment Mode'],textposition='outside')
        coll11,coll22=st.columns((2))
        with coll11:
            with st.expander('Click to view Pie chart for mode of payment'):
                st.plotly_chart(fig,use_container_width=True)
        with coll22:
            with st.expander('Click to view data frame for mode of payment'):
                st.write(payment_mode)
    
    sales=sales_data_layers[["Date","Sales"]]
    expense=expense_data_layers[['Date','Bill']]
    sales['Date']=pd.to_datetime(sales['Date'])
    expense['Date']=pd.to_datetime(expense['Date'])
    sales_dataframe=sales.groupby('Date')['Sales'].sum().reset_index()
    expense_dataframe=expense.groupby("Date")['Bill'].sum().reset_index()
    merged_sales_expense=pd.merge(sales_dataframe, expense_dataframe, on='Date',how='outer').sort_values(by="Date")
    merged_sales_expenses=merged_sales_expense.fillna(0)
    merged_sales_expenses['Profit']=merged_sales_expense['Sales']-merged_sales_expenses['Bill']
    merged_sales_expenses["Date"]=pd.to_datetime(merged_sales_expenses["Date"])
    start_date2= merged_sales_expenses["Date"].min()
    end_date2=merged_sales_expenses["Date"].max()
    col1,col2=st.columns((2))
    with col1:
        date11=pd.to_datetime(st.date_input("Begin on", start_date2)) 
    with col2:
        date21=pd.to_datetime(st.date_input("End on",end_date2))
    if st.button("Analyse profit"):    
        fig=px.line(merged_sales_expenses,x='Date',y=['Sales','Bill','Profit'], labels={'Sales':'Amount'},height=500,width=1000,template='gridon')
        st.plotly_chart(fig,use_container_width=True)
        st.write(merged_sales_expenses)
            
    
else:
    st.subheader('Record New Sales :point_down:')
    sales_date = st.date_input('Customer service purchase Date( YYYY/MM/DD)', key="sales_date")
    products = inventory_data_layers['Product'].tolist()  # Get product list from inventory
    selected_products = st.multiselect('Select Products(s)', options=products)
    sales = st.text_input('Amount paid for product (separate prices by commas)', key="sales_sales")
    sales_quantity= st.text_input('Quantity(s) (Separate Quantity by commas)',key="sales_quantity")
    payment_mode = st.selectbox('Payment Mode', ['Cash', 'Bank Account', 'M-pesa', 'Others'])

    if st.button('Add Entry'):
        if sales_date and selected_products and sales and sales_quantity and payment_mode:  # Check if all fields are filled
            for product,sales, quantity in zip(selected_products, map(str, sales.split(',')) ,map(int, sales_quantity.split(','))):
                sales_list = [float(s.strip()) for s in sales.split(",")]
                add_sales_layers_entry(sales_date, product, sales_list, [quantity], payment_mode)  # Convert to integer
            st.sidebar.success('Entry Added Successfully!')
            sales_data_layers.to_csv("saleslayers.csv", index=False)  # Save the updated DataFrame to CSV
            inventory_data_layers.to_csv("inventorylayers.csv", index=False)  # Save the updated inventory DataFrame to CSV
        else:
            st.sidebar.error('Please fill all fields before adding the entry.')

    # Display the sales data
    st.subheader('Sales Data')
    display_sales_data_layers()
      # Option to delete rows from sales data
    st.subheader('Delete Rows from Sales Data')
    rows_to_delete_sales = st.multiselect("Select rows to delete from Sales Data", options=sales_data_layers.index.tolist())
    if st.button("Delete Selected Rows from Sales Data"):
        sales_data_layers.drop(rows_to_delete_sales, inplace=True)
        sales_data_layers.to_csv("saleslayers.csv", index=False)
        st.success("Selected rows deleted from Sales Data.")
    
    st.subheader('Manage Inventory')
    inventory_action = st.radio("Select action", ["View Inventory", "Add or Update Inventory"])

    if inventory_action == "View Inventory":
        st.subheader('Inventory Data')
        display_inventory_data_layers()
            # Option to delete rows from inventory data
        st.subheader('Delete Rows from Inventory Data')
        rows_to_delete_inventory = st.multiselect("Select rows to delete from Inventory Data", options=inventory_data_layers.index.tolist())
        if st.button("Delete Selected Rows from Inventory Data"):
            inventory_data_layers.drop(rows_to_delete_inventory, inplace=True)
            inventory_data_layers.to_csv("inventorylayers.csv", index=False)
            st.success("Selected rows deleted from Inventory Data.")
    else:
        st.subheader('Add or Update Inventory')
        inventory_date = st.date_input('Inventory Date', key="inventory_date")
        inventory_product = st.text_input('Product')
        inventory_quantity = st.number_input('Quantity', key="inventory_quantity")

        if st.button('Add/Update Inventory'):
            if inventory_date and inventory_product and inventory_quantity:  # Check if all fields are filled
                add_or_update_inventory_layers(inventory_date, inventory_product, inventory_quantity)
                st.success('Inventory Updated Successfully!')
                inventory_data_layers.to_csv("inventorylayers.csv", index=False)  # Save the updated inventory DataFrame to CSV
            else:
                st.error('Please fill all fields before updating the inventory.') 
                
    st.subheader('Add expense')
    expense_date = st.date_input('Expense Date', key="Expense_date")
    expense_expense = st.text_input('Expense')
    expense_bill = st.number_input('Bill')

    if st.button('Add Expense'):
        if expense_date and expense_expense and expense_bill:  # Check if all fields are filled
            add_expense_layers(expense_date, expense_expense, expense_bill)
            st.success('Expense Updated Successfully!')
            expense_data_layers.to_csv("expenselayers.csv", index=False)  # Save the updated inventory DataFrame to CSV
        else:
            st.error('Please fill all fields before adding the expense.') 
    display_expense_data_layers()
    st.subheader('Delete Rows from expense Data')
    rows_to_delete_expense = st.multiselect("Select rows to delete from expense Data", options=expense_data_layers.index.tolist())
    if st.button("Delete Selected Rows from expense Data"):
        expense_data_layers.drop(rows_to_delete_expense, inplace=True)
        expense_data_layers.to_csv("expenseLayers.csv", index=False)
        st.success("Selected rows deleted from expense Data.")
    
    st.subheader('Add  Egg Production')
    egg_date = st.date_input('Date layed', key="Layed_date")
    bird_number = st.text_input('Number of birds')
    number_of_eggs = st.number_input('Number of eggs')

    if st.button('Add Egg Production'):
        if egg_date and bird_number and number_of_eggs:  # Check if all fields are filled
            add_egg_production(egg_date, bird_number, number_of_eggs)
            st.success('Egg production Updated Successfully!')
            egg_production.to_csv("eggproduction.csv", index=False)  # Save the updated inventory DataFrame to CSV
        else:
            st.error('Please fill all fields before adding the egg production.') 
    display_egg_production()
    st.subheader('Delete Rows from egg production Data')
    rows_to_delete_ep = st.multiselect("Select rows to delete from egg production Data", options=egg_production.index.tolist())
    if st.button("Delete Selected Rows from egg production Data"):
        egg_production.drop(rows_to_delete_ep, inplace=True)
        egg_production.to_csv("eggproduction.csv", index=False)
        st.success("Selected rows deleted from egg production Data.")


st.title("CHICK'S SECTION")
meat_action = st.radio("Select Page", ["Record", "Analysis"])
if meat_action =="Analysis":
    st.title("Chicks Business Analytics :bar_chart:")
    inventory_data_meat["Date"]=pd.to_datetime(inventory_data_meat["Date"])
    start_date13= inventory_data_meat["Date"].min()
    end_date13=inventory_data_meat["Date"].max()
    col1,col2=st.columns((2))
    with col1:
        date113=pd.to_datetime(st.date_input("Start", start_date13)) 
    with col2:
        date213=pd.to_datetime(st.date_input("End",end_date13)) 
    chicks_data=inventory_data_meat[(inventory_data_meat["Date"]>=date113)&(inventory_data_meat["Date"]<=date213)].copy()
    filtered_chicks_data=st.sidebar.multiselect("Select your Chick Group",chicks_data["Group"].unique())
    if not filtered_chicks_data:
        filtered_chicks_data = chicks_data.copy()
    else:
        filtered_chicks_data =chicks_data[chicks_data["Group"].isin(filtered_chicks_data)]
    filtered_chicks_data1 = st.sidebar.multiselect("Select The Week for Analysis",filtered_chicks_data["Week"].unique())
    if not filtered_chicks_data1:
        filtered_chicks_data1=filtered_chicks_data.copy()
    else:
        filtered_chicks_data1=filtered_chicks_data[filtered_chicks_data['Week'].isin(filtered_chicks_data1)]
 
    filtered_chicks_data1['Chick Sales']= filtered_chicks_data1['Market Price']*filtered_chicks_data1['Number of Chicks']
    filtered_chicks_data1['Cumaulative Cost']=filtered_chicks_data1['Cost'].cumsum()
    filtered_chicks_data1['Profit']=filtered_chicks_data1['Chick Sales']-filtered_chicks_data1['Cumaulative Cost']
    st.write(filtered_chicks_data1)
    if st.button('Analyse your Profit Sales and Expenses'):
        chick_line_graph=px.line(filtered_chicks_data1,x='Date',y=['Cumaulative Cost','Chick Sales','Profit'],height=500, width=1000,template='gridon')
        st.plotly_chart(chick_line_graph,use_container_width=True)
        st.write('Expenses Costs')
        expense_cost=filtered_chicks_data1.groupby('Expense')['Cost'].sum().sort_values(ascending=True).reset_index()
        st.write(expense_cost)
        bar_expense_cost=px.bar(expense_cost, x='Expense',y='Cost',height=500,width=1000,template='gridon')
        st.plotly_chart(bar_expense_cost,use_container_width=True)
    
    sales_data_meat["Date"]=pd.to_datetime(sales_data_meat["Date"])
    start_date14= sales_data_meat["Date"].min()
    end_date14=sales_data_meat["Date"].max()
    col1,col2=st.columns((2))
    with col1:
        date114=pd.to_datetime(st.date_input("Starting from", start_date14)) 
    with col2:
        date214=pd.to_datetime(st.date_input("Ending on",end_date14)) 
    chicks_sales_data=sales_data_meat[(sales_data_meat["Date"]>=date114)&(sales_data_meat["Date"]<=date214)].copy()
    
    filtered_chicks_sales_data=st.sidebar.multiselect("Select your Sold product",chicks_sales_data["Product"].unique())
    if not filtered_chicks_sales_data:
        filtered_chicks_sales_data = chicks_sales_data.copy()
    else:
        filtered_chicks_sales_data =chicks_sales_data[chicks_sales_data["Product"].isin(filtered_chicks_sales_data)]
    
    product_sold= filtered_chicks_sales_data.groupby('Product')['Sales'].sum().sort_values(ascending=True).reset_index()
    st.write(product_sold)
    product_line=px.bar(product_sold,x='Product',y='Sales',height=500,width=1000, template='seaborn')
    st.plotly_chart(product_line,use_container_width=True)
    products_payment=filtered_chicks_sales_data.groupby('Payment Mode')['Sales'].sum().sort_values(ascending=True).reset_index()
    st.write(products_payment)
    product_pie=px.pie(products_payment,values='Sales',hole=0.5)
    st.write(product_pie,use_container_width=True)
    
    expense_datas=expense_data_meat[['Date','Bill']]
    sales_datas=sales_data_meat[['Date','Sales']]
    expense_datas['Date']=pd.to_datetime(expense_datas['Date'])
    sales_datas['Date']=pd.to_datetime(sales_datas['Date'])
    traexpense_datas= expense_datas.groupby('Date')['Bill'].sum().reset_index()
    trasales_datas=sales_datas.groupby('Date')['Sales'].sum().reset_index()
    merged_sale_expe=pd.merge(traexpense_datas,trasales_datas, on='Date',how='outer').sort_values(by="Date")
    merged_sale_expe=merged_sale_expe.fillna(0)
    st.write(merged_sale_expe)
    merged_sale_expe['Profit']=merged_sale_expe['Sales']-merged_sale_expe['Bill']
    merged_sale_expe["Date"]=pd.to_datetime(merged_sale_expe["Date"])
    start_date15= merged_sale_expe["Date"].min()
    end_date15=merged_sale_expe["Date"].max()
    col1,col2=st.columns((2))
    with col1:
        date115=pd.to_datetime(st.date_input("StartingFrom", start_date15)) 
    with col2:
        date215=pd.to_datetime(st.date_input("EndingOn",end_date15)) 
    chicks_expense_data=merged_sale_expe[(merged_sale_expe["Date"]>=date115)&(merged_sale_expe["Date"]<=date215)].copy()
    
    figs=px.line(chicks_expense_data,x='Date',y=['Bill','Sales'],height=500,width=1000,template='seaborn')
    st.plotly_chart(figs,use_container_width=True)
    chicks_expense_data['Month']=chicks_expense_data['Date'].dt.month
    month_profit=chicks_expense_data[['Month','Profit']]
    monthly_profit=month_profit.groupby('Month')['Profit'].sum().reset_index()
    st.write(monthly_profit)
    figp=px.bar(monthly_profit,x='Month',y='Profit',height=500,width=1000,template='seaborn')
    st.plotly_chart(figp,use_container_width=True)
    total_expense=expense_data_meat.groupby('Expense')['Bill'].sum().sort_values(ascending=True).reset_index()
    st.write(total_expense)
    total_sales=sales_data_meat.groupby('Product')['Sales'].sum().sort_values(ascending=True).reset_index()
    st.write(total_sales)
    w=total_sales['Sales'].sum()
    x=total_expense['Bill'].sum()
    y=w-x
    col1,col2,col3=st.columns(3)
    with col1:
        with st.expander('View Total Sales'):
            st.write(w)
    with col2:
        with st.expander('View Total Expenses'):
            st.write(x)
    with col3:
        with st.expander('View Total Profit'):
            st.write(y)
else:
    st.subheader('Record New Sales :point_down:')
    sales_date = st.date_input('Customer service purchase Date( YYYY/MM/DD)', key="sale_date")
    selected_products = st.text_input('Product Sold Out')
    sales = st.text_input('amount paid for product (separate prices by commas)', key="sale_sales")
    sales_quantity= st.text_input('quantity(s) (Separate Quantity by commas)',key="sale_quantity")
    payment_mode = st.text_input('payment Mode', ['Cash', 'Bank Account', 'M-pesa', 'Others'])

    if st.button('add Entry'):
        if sales_date and selected_products and sales and sales_quantity and payment_mode:  # Check if all fields are filled
            
            add_sales_meat_entry(sales_date, selected_products, sales, sales_quantity, payment_mode)  # Convert to integer
            st.sidebar.success('Entry Added successfully!')
            sales_data_meat.to_csv("salesmeat.csv", index=False)  # Save the updated DataFrame to CSV
            inventory_data_meat.to_csv("inventorymeat.csv", index=False)  # Save the updated inventory DataFrame to CSV
        else:
            st.sidebar.error('Please fill all fields before adding the entry.')

    # Display the sales data
    st.subheader('Sales Data')
    display_sales_data_meat()
      # Option to delete rows from sales data
    st.subheader('Delete rows from Sales Data')
    rows_to_delete_sales = st.multiselect("Select Rows to delete from Sales Data", options=sales_data_meat.index.tolist())
    if st.button("Delete selected Rows from Sales Data"):
        sales_data_meat.drop(rows_to_delete_sales, inplace=True)
        sales_data_meat.to_csv("salesmeat.csv", index=False)
        st.success("Selected rows deleted from Sales Data.")
                
    st.subheader('Add an expense')
    expense_date = st.date_input('expense Date', key="expense_date")
    expense_expense = st.text_input('expense')
    expense_bill = st.number_input('bill')

    if st.button('Add an Expense'):
        if expense_date and expense_expense and expense_bill:  # Check if all fields are filled
            add_expense_meat(expense_date, expense_expense, expense_bill)
            st.success('Expense Updated successfully!')
            expense_data_meat.to_csv("expensemeat.csv", index=False)  # Save the updated inventory DataFrame to CSV
        else:
            st.error('please fill all fields before adding the expense.') 
    display_expense_data_meat()
    st.subheader('Delete Row from expense Data')
    rows_to_delete_expense = st.multiselect("Select rows to delete from expense data", options=expense_data_meat.index.tolist())
    if st.button("Delete Selected Row from expense Data"):
        expense_data_meat.drop(rows_to_delete_expense, inplace=True)
        expense_data_meat.to_csv("expensemeat.csv", index=False)
        st.success("Selected rows deleted from expense data.")
        
    st.subheader('Add a Chick expense')
    chick_date = st.date_input('chick input Date', key="chick_date")
    chick_week = st.text_input('Chicks Week')
    chick_expense = st.text_input('Chick Expenses')
    chick_expense_estimatecost = st.text_input('Chick Expenses Estimated cost')
    chick_market_price = st.text_input('Chick market price')
    chicks_total=st.text_input('Total number of Chicks at current time')
    chicks_Group=st.text_input('Group of Chicks')
    

    if st.button('Add a Chick Expense'):
        if chick_date and chick_week and chick_expense and chick_expense_estimatecost and chick_market_price and chicks_total and chicks_Group:  # Check if all fields are filled
            add_expense_chick( chick_date,chick_week,chick_expense,chick_expense_estimatecost,chick_market_price,chicks_total,chicks_Group)
            st.success('Expense Updated successfully!')
            inventory_data_meat.to_csv("inventorymeat.csv", index=False)  # Save the updated inventory DataFrame to CSV
        else:
            st.error('please fill all required chicks fields before adding the expense.') 
    display_inventory_data_meat()
    st.subheader('Delete Row from Chicks expense Data')
    rows_to_delete_expe = st.multiselect("Select rows to delete from Chick expense data", options=inventory_data_meat.index.tolist())
    if st.button("Delete Selected Row/rows from chick expense Data"):
        inventory_data_meat.drop(rows_to_delete_expe, inplace=True)
        inventory_data_meat.to_csv("inventorymeat.csv", index=False)
        st.success("Selected rows deleted from Chicks expense data.")      