
# ENV py31013
# THIS IS dynamic tool:
# # python -m streamlit run  D:\Projects_inDev\INVESTMENT_DSS\beergame_sample_example\3_beergame_WIP.py
import os
import streamlit as st
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize
from scipy.stats import norm
import random
import matplotlib.pyplot as plt


# #default paramtere
IND_ALL_ECHELONS_COMMON_INFO = False
iDISPLAY_FINAL_STATS = False
iROLE = 0
number_of_turns = 11
supplier_lead_time = [1,1,1,1] # -1 => same week / instantaneous delivery# LETS RUN FOR RETAILER:
initial_stock = [15,15,15,15]
initial_backlog = [0,0,0,0]
cntfacility = [1,1,1,1]  # each number reprsents count of each facility, from left to right; 1-retialer, 1-wholeseller, 1-distributor & 1-manufacturer

if "incoming_demand" not in st.session_state:
    incoming_demand = [[],[],[],[]]
    st.session_state['incoming_demand'] = incoming_demand

if "stocks" not in st.session_state:
    stocks = [[],[],[],[]]
    st.session_state['stocks'] = stocks


if "shipped_order" not in st.session_state:
    shipped_order = [[],[],[],[]]
    st.session_state['shipped_order'] = shipped_order


if "outgoing_order_arrival_schedule" not in st.session_state:
    outgoing_order_arrival_schedule = []
    outgoing_order_arrival_schedule.append([0] * (number_of_turns + supplier_lead_time[0] + 1))
    outgoing_order_arrival_schedule.append([0] * (number_of_turns + supplier_lead_time[0] + 1))
    outgoing_order_arrival_schedule.append([0] * (number_of_turns + supplier_lead_time[0] + 1))
    outgoing_order_arrival_schedule.append([0] * (number_of_turns + supplier_lead_time[0] + 1))
    st.session_state['outgoing_order_arrival_schedule'] = outgoing_order_arrival_schedule

if "outgoing_order_arrival_actuals" not in st.session_state:
    outgoing_order_arrival_actuals = []
    outgoing_order_arrival_actuals.append([0] * (number_of_turns + supplier_lead_time[0] + 1))
    outgoing_order_arrival_actuals.append([0] * (number_of_turns + supplier_lead_time[0] + 1))
    outgoing_order_arrival_actuals.append([0] * (number_of_turns + supplier_lead_time[0] + 1))
    outgoing_order_arrival_actuals.append([0] * (number_of_turns + supplier_lead_time[0] + 1))
    st.session_state['outgoing_order_arrival_actuals'] = outgoing_order_arrival_actuals


if "backlog" not in st.session_state:
    backlog = [[],[],[],[]]
    st.session_state['backlog'] = backlog


if "inventory" not in st.session_state:
    inventory = [[],[],[],[]]
    st.session_state['inventory'] = inventory


if "mydata" not in st.session_state:
    mydata = pd.DataFrame({"col 0": [],
                           "col 1": []})
    st.session_state['mydata'] = mydata

if "counter" not in st.session_state:
    counter = 0
    st.session_state['counter'] = counter


if "runtime_lstOflsts_incoming_demand" not in st.session_state:
    runtime_lstOflsts_incoming_demand = [[], [], [], []]
    st.session_state['runtime_lstOflsts_incoming_demand'] = runtime_lstOflsts_incoming_demand


if "runtime_lstOflsts_eoq_qty_decision" not in st.session_state:
    runtime_lstOflsts_eoq_qty_decision = [[], [], [], []]
    st.session_state['runtime_lstOflsts_eoq_qty_decision'] = runtime_lstOflsts_eoq_qty_decision


# persist state of dataframe
if "results0" not in st.session_state:
    results0 = pd.DataFrame({"demanded": [],
                                     "EOQed": [],
                                     "actual_arrivals": [],
                                     "stocks_eop": [],
                                     "backlogs_eop": [],
                                     "Shipped_eop": []
                                     })
    st.session_state['results0'] = results0


if "results1" not in st.session_state:
    results1 = pd.DataFrame({"demanded": [],
                                     "EOQed": [],
                                     "actual_arrivals": [],
                                     "stocks_eop": [],
                                     "backlogs_eop": [],
                                     "Shipped_eop": []
                                     })
    st.session_state['results1'] = results1

if "results2" not in st.session_state:
    results2 = pd.DataFrame({"demanded": [],
                                     "EOQed": [],
                                     "actual_arrivals": [],
                                     "stocks_eop": [],
                                     "backlogs_eop": [],
                                     "Shipped_eop": []
                                     })
    st.session_state['results2'] = results2


if "results3" not in st.session_state:
    results3 = pd.DataFrame({"demanded": [],
                                     "EOQed": [],
                                     "actual_arrivals": [],
                                     "stocks_eop": [],
                                     "backlogs_eop": [],
                                     "Shipped_eop": []
                                     })
    st.session_state['results3'] = results3



if "lst_eoq_ui" not in st.session_state:
    st.session_state['lst_eoq_ui'] = []



## LETS ASSIGN session-state to variables
##
#mydata = st.session_state['mydata']
counter = st.session_state['counter']
incoming_demand = st.session_state['incoming_demand']
stocks = st.session_state['stocks']
shipped_order = st.session_state['shipped_order']
outgoing_order_arrival_schedule = st.session_state['outgoing_order_arrival_schedule']
outgoing_order_arrival_actuals = st.session_state['outgoing_order_arrival_actuals']
backlog = st.session_state['backlog']
# inventory = st.session_state['inventory']


runtime_lstOflsts_incoming_demand = st.session_state['runtime_lstOflsts_incoming_demand']
runtime_lstOflsts_eoq_qty_decision = st.session_state['runtime_lstOflsts_eoq_qty_decision']

lst_eoq_ui = st.session_state['lst_eoq_ui']

results0 = st.session_state['results0']
results1 = st.session_state['results1']
results2 = st.session_state['results2']
results3 = st.session_state['results3']



# COSTS
ordering_or_setup_cost_perorder = 5  ## K like setup octs
cost_per_unit = 15   # unit purchase cost
storageOrHolding_cost_per_unit = 0.5
shortageOrEmergencyOrBackordered_cost_per_unit = 1 # placed end of week and delievered instantaaneously


## following objects will be required to track...scheduled EOQs vs whts actually delivered by upper echelon!

def fsimulatebeergame(isim,current_user_role,mu_sigma_eoq):
    """
    :param isim: time-period / run
    :param user_role: what role you are assuming
    :return: it updates runtime_lstOflsts_incoming_demand object
    mu_sigma_eoq = [10,3,5]
    """
    mu = int(mu_sigma_eoq[0])
    sigma = int(mu_sigma_eoq[1])
    user_ordered_eoq = int(mu_sigma_eoq[2])



    # loop through 1-facility at a time & create/update lstOflsts to store numbers
    for user_role in range(0, len(cntfacility)): ## for each facility get/generate demand & EOQs
        # for each
        if current_user_role == user_role:
            # CALCULATE DEMAND: generate DEMAND given mu & sigma for retailer
            usergiven_or_generate_demand = int(random.normalvariate(mu, sigma))     # for hard values we can use >>> lstOflsts_incoming_demand[user_role][isim]
            # save this value (this will be used inside runs)
            runtime_lstOflsts_incoming_demand[user_role].append(usergiven_or_generate_demand)

            # CALCULATE EOQ:  How much to order ? EOQ-decision ? this is a user input
            # When we are decding EOQ, we are deciding EOQ-order at the EOP post ensuring inventory/backlog & incoming demand &/or arrivals ...but for now this is a user input

            usergiven_or_generate_eoq_decision = user_ordered_eoq  # for hard values we can use >>> lstOflsts_eoq_qty_decision[user_role][isim]
            runtime_lstOflsts_eoq_qty_decision[user_role].append(usergiven_or_generate_eoq_decision)



            # CALCULATE stock-availability ? stocks[i-1] + incoming_deliveries (these are the actuals that we reeived )
            if isim == 0:
                actual_arrival = outgoing_order_arrival_schedule[user_role][isim]  ## this is given by user or function-generated value , here actual delivered could be reduced
                outgoing_order_arrival_actuals[user_role][isim] = actual_arrival  # lets update arrivals array
                stock_available = initial_stock[user_role] + outgoing_order_arrival_actuals[user_role][isim]
                stocks[user_role].append(stock_available)
                # backorder
                backlog[user_role].append(initial_backlog[user_role])

                #generate_EOQ_to_order = np.max([stock_available,runtime_lstOflsts_incoming_demand[user_role],backlog[user_role]])

            else:
                actual_arrival = outgoing_order_arrival_schedule[user_role][isim]   ## this is given by user or function-generated value
                outgoing_order_arrival_actuals[user_role][isim] = actual_arrival  # lets update arrivals array
                stock_available = stocks[user_role][isim - 1] + outgoing_order_arrival_actuals[user_role][isim]
                # lets append this value
                stocks[user_role].append(stock_available)
                backlog[user_role].append(backlog[user_role][isim - 1])


            # when will this EOQ arrive ?..schduled & arriavls will be same ...no lead-time variability in the qty for now
            # the lead-times are at least 1-week & therefoew it can be here below above section...
            outgoing_order_arrival_schedule[user_role][isim + supplier_lead_time[user_role] + 1] = usergiven_or_generate_eoq_decision
            outgoing_order_arrival_actuals[user_role][isim + supplier_lead_time[user_role] + 1] = usergiven_or_generate_eoq_decision

            # based on the stocks-levels, fulfill backlogs and incoming demand as follows;
            ship_qty_backlogged = 0
            ship_qty_demands = 0
            # """
            # we can serve incoming-demand+backorders only when we have stock-availability
            # else ---> everything is backordered
            #
            # """

            if stocks[user_role][isim] > 0:  #
                if backlog[user_role][isim] > 0:  # if so fulfill as-much as you can
                    if backlog[user_role][isim] > stocks[user_role][isim]:
                        ship_qty_backlogged = stocks[user_role][isim]
                        # reduce stocks & backlogs QTYs
                        stocks[user_role][isim] = stocks[user_role][isim] - ship_qty_backlogged
                        backlog[user_role][isim] = backlog[user_role][isim] - ship_qty_backlogged

                    if backlog[user_role][isim] <= stocks[user_role][isim]:
                        ship_qty_backlogged = backlog[user_role][isim]
                        # reduce stocks & backlogs QTYs
                        stocks[user_role][isim] = stocks[user_role][isim] - ship_qty_backlogged
                        backlog[user_role][isim] = 0

                if runtime_lstOflsts_incoming_demand[user_role][isim] > 0:
                    if runtime_lstOflsts_incoming_demand[user_role][isim] > stocks[user_role][isim]:  # some part will be fullfilled from stocks & some will be backlogged
                        # incoming_demand = stocks + backlogg
                        ship_qty_demands = stocks[user_role][isim]
                        # reduce stocks & backlogs QTYs
                        stocks[user_role][isim] = stocks[user_role][isim] - ship_qty_demands
                        backlog[user_role][isim] = backlog[user_role][isim] + runtime_lstOflsts_incoming_demand[user_role][isim] - ship_qty_demands  # remaining will be backlogged

                    if runtime_lstOflsts_incoming_demand[user_role][isim] <= stocks[user_role][isim]:  # all demadn can be served
                        ship_qty_demands = runtime_lstOflsts_incoming_demand[user_role][isim]
                        # reduce stocks & backlogs QTYs
                        stocks[user_role][isim] = stocks[user_role][isim] - ship_qty_demands
                        # no change in backlog[0][i]

                # Lets updted shipped qty
                shipped_order[user_role].append(ship_qty_backlogged + ship_qty_demands)


            elif stocks[user_role][isim] == 0:  # just increase the backlogs
                backlog[user_role][isim] = backlog[user_role][isim - 1] + runtime_lstOflsts_incoming_demand[user_role][isim]
                shipped_order[user_role].append(0)

            else:
                print("ERROR LINE-147: stocks cannot be negative !!!")
                quit()



        # elif current_user_role > user_role: # since we are only allowing retailer-user, this condition is not getting executed for now (unless we allow other roles to play for user)
        #     # CALCULATE: DEMAND get the customer-demand
        #     usergiven_or_generate_demand = lstOflsts_incoming_demand[user_role][isim]  # just get the user given value @ ith posiiton/isim
        #     # save this value (this will be used inside runs)
        #     runtime_lstOflsts_incoming_demand[user_role].append(usergiven_or_generate_demand)


        elif current_user_role < user_role:
            # since the user is retailer....whatever retailer orders that will be wholeseller`s demand!
            # wholeseller - demand = EOQ from retailer
            # wholeseller - EOQ = function or given values

            # DEMAND-values
            # retailers-EOQ is wholeseller`s demand
            usergiven_or_generate_demand = runtime_lstOflsts_eoq_qty_decision[user_role-1][isim]   # just get the user given value @ ith posiiton/isim
            # save this value
            runtime_lstOflsts_incoming_demand[user_role].append(usergiven_or_generate_demand)


            # EOQ
            # CALCULATE EOQ:  How much to order EOQ-decision ? this is a user input
            # we are deciding EOQ-order at the EOP post ensuring inventory/backlog & incoming demand &/or arrivals
            # EOQ is based at the least on  = available stocks[i-1] + expected demand this week(runtime_lstOflsts_incoming_demand) + backlogs[i-1]

            if isim == 0:
                actual_arrival = outgoing_order_arrival_schedule[user_role][isim]  ## this is given by user or function-generated value , here actual delivered could be reduced
                outgoing_order_arrival_actuals[user_role][isim] = actual_arrival  # lets update arrivals array
                stock_available = initial_stock[user_role] + outgoing_order_arrival_actuals[user_role][isim]
                stocks[user_role].append(stock_available)
                # backorder
                backlog[user_role].append(initial_backlog[user_role])

            else:
                actual_arrival = outgoing_order_arrival_schedule[user_role][isim]   ## this is given by user or function-generated value
                outgoing_order_arrival_actuals[user_role][isim] = actual_arrival  # lets update arrivals array
                stock_available = stocks[user_role][isim - 1] + outgoing_order_arrival_actuals[user_role][isim]
                # lets append this value
                stocks[user_role].append(stock_available)
                backlog[user_role].append(backlog[user_role][isim - 1])


            # lets calcuate apropriate stock/backorder & based on that finally generate EOQ to be orderd
            # based on the stocks-levels, fulfill backlogs and incoming demand as follows;
            ship_qty_backlogged = 0
            ship_qty_demands = 0
            # """
            # we can serve incoming-demand+backorders only when we have stock-availability
            # else ---> everything is backordered
            #
            # """

            if stocks[user_role][isim] > 0:  #
                if backlog[user_role][isim] > 0:  # if so fulfill as-much as you can
                    if backlog[user_role][isim] > stocks[user_role][isim]:
                        ship_qty_backlogged = stocks[user_role][isim]
                        # reduce stocks & backlogs QTYs
                        stocks[user_role][isim] = stocks[user_role][isim] - ship_qty_backlogged
                        backlog[user_role][isim] = backlog[user_role][isim] - ship_qty_backlogged

                    if backlog[user_role][isim] <= stocks[user_role][isim]:
                        ship_qty_backlogged = backlog[user_role][isim]
                        # reduce stocks & backlogs QTYs
                        stocks[user_role][isim] = stocks[user_role][isim] - ship_qty_backlogged
                        backlog[user_role][isim] = 0

                if runtime_lstOflsts_incoming_demand[user_role][isim] > 0:
                    if runtime_lstOflsts_incoming_demand[user_role][isim] > stocks[user_role][isim]:  # some part will be fullfilled from stocks & some will be backlogged
                        # incoming_demand = stocks + backlogg
                        ship_qty_demands = stocks[user_role][isim]
                        # reduce stocks & backlogs QTYs
                        stocks[user_role][isim] = stocks[user_role][isim] - ship_qty_demands
                        backlog[user_role][isim] = backlog[user_role][isim] + runtime_lstOflsts_incoming_demand[user_role][isim] - ship_qty_demands  # remaining will be backlogged

                    if runtime_lstOflsts_incoming_demand[user_role][isim] <= stocks[user_role][isim]:  # all demadn can be served
                        ship_qty_demands = runtime_lstOflsts_incoming_demand[user_role][isim]
                        # reduce stocks & backlogs QTYs
                        stocks[user_role][isim] = stocks[user_role][isim] - ship_qty_demands
                        # no change in backlog[0][i]

                # Lets updted shipped qty
                shipped_order[user_role].append(ship_qty_backlogged + ship_qty_demands)


            elif stocks[user_role][isim] == 0:  # just increase the backlogs
                backlog[user_role][isim] = backlog[user_role][isim - 1] + runtime_lstOflsts_incoming_demand[user_role][isim]
                shipped_order[user_role].append(0)

            else:
                print("ERROR LINE-147: stocks cannot be negative !!!")
                quit()

            # we will observe current-values of stocks[user_role][isim], runtime_lstOflsts_incoming_demand[user_role][isim], backlog[user_role][isim]
            generate_EOQ_to_order = np.max([stocks[user_role][isim],runtime_lstOflsts_incoming_demand[user_role][isim],backlog[user_role][isim]])

            # Lets save this generated EOQ for this entity
            runtime_lstOflsts_eoq_qty_decision[user_role].append(generate_EOQ_to_order)

            # & WHEN will this EOQ order arrive ???
            # the lead-times are at least 1-week & therefoew it can be here below above section...
            outgoing_order_arrival_schedule[user_role][isim + supplier_lead_time[user_role] + 1] = generate_EOQ_to_order
            outgoing_order_arrival_actuals[user_role][isim + supplier_lead_time[user_role] + 1] = generate_EOQ_to_order


        else:
            print("ERROR line-402: facility not found")
            quit()


    facility = 0
    results0 = pd.DataFrame({
        "demanded": runtime_lstOflsts_incoming_demand[facility],
        "EOQed": runtime_lstOflsts_eoq_qty_decision[facility],
        "actual_arrivals": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
        "stocks_eop": stocks[facility],
        "backlogs_eop":backlog[facility],
        "Shipped_eop": shipped_order[facility]

        #"scheduled_arrivals_qty_bop": outgoing_order_arrival_schedule[0][0:len(stocks[0])],

    })

    facility = 1
    results1 = pd.DataFrame({
        "demanded": runtime_lstOflsts_incoming_demand[facility],
        "EOQed": runtime_lstOflsts_eoq_qty_decision[facility],
        "actual_arrivals": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
        "stocks_eop": stocks[facility],
        "backlogs_eop":backlog[facility],
        "Shipped_eop": shipped_order[facility]

        #"scheduled_arrivals_qty_bop": outgoing_order_arrival_schedule[0][0:len(stocks[0])],

    })

    facility = 2
    results2 = pd.DataFrame({
        "demanded": runtime_lstOflsts_incoming_demand[facility],
        "EOQed": runtime_lstOflsts_eoq_qty_decision[facility],
        "actual_arrivals": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
        "stocks_eop": stocks[facility],
        "backlogs_eop":backlog[facility],
        "Shipped_eop": shipped_order[facility]

        #"scheduled_arrivals_qty_bop": outgoing_order_arrival_schedule[0][0:len(stocks[0])],

    })

    facility = 3
    results3 = pd.DataFrame({
        "demanded": runtime_lstOflsts_incoming_demand[facility],
        "EOQed": runtime_lstOflsts_eoq_qty_decision[facility],
        "actual_arrivals": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
        "stocks_eop": stocks[facility],
        "backlogs_eop":backlog[facility],
        "Shipped_eop": shipped_order[facility]

        #"scheduled_arrivals_qty_bop": outgoing_order_arrival_schedule[0][0:len(stocks[0])],

    })


    return results0, results1, results2, results3





st.set_page_config(layout="wide")

st.title("BEER GAME : A SCM TOOL TO UNDERSTAND 'bullwhip effect' ")
st.subheader("You are playing as  = 'RETAILER' ")


with st.container():
    # USER-INPUT SECTION - 2
    col1, col2 = st.columns([1,1])
    with col1:
        #iROLE = 0 --definied at the top

        if "mean_demand" not in st.session_state:
            st.session_state["mean_demand"] = 0

        if "stdev_demand" not in st.session_state:
            st.session_state["stdev_demand"] = 0

        st.text("\n")
        st.text("USER INPUT: Demand Distribution Parameters")
        st.session_state["mean_demand"] = st.number_input("Mean", min_value=5.0)
        st.session_state["stdev_demand"] = st.number_input("Std Deviation", min_value=1.0)

        mu = st.session_state["mean_demand"]
        sigma = st.session_state["stdev_demand"]

        st.text("\n")
        st.text("USER INPUT: EOQ order quantity")
        user_eoq_qty = st.number_input("EOQ Order-Quantity)", min_value=0.0)
        st.text("NOTE: this EOQ order has default arrival lead time = 1-week, i.e if you order in say 1st week, the order will arrive starting 3rd week")
        st.text("\n")

    with col2:

        if st.button("Next Week"):

            # call beer-game
            if counter < number_of_turns :
                results0, results1, results2, results3 = fsimulatebeergame(isim = counter, current_user_role = iROLE, mu_sigma_eoq=[mu,sigma,user_eoq_qty])

                #newdata = pd.DataFrame(np.random.randn(2, 2), columns=("col %d" % i for i in range(2)))
                #mydata = pd.concat([mydata, newdata], axis=0)
                # st.session_state['mydata'] = mydata

                # increment counter
                counter = counter + 1

                # re-assign session_variables , as they have been updated
                st.session_state['counter'] = counter

                ## folliwng are user within function , so they need to be updated
                st.session_state['incoming_demand'] = incoming_demand
                st.session_state['stocks'] = stocks
                st.session_state['shipped_order'] = shipped_order
                st.session_state['outgoing_order_arrival_schedule'] = outgoing_order_arrival_schedule
                st.session_state['outgoing_order_arrival_actuals'] = outgoing_order_arrival_actuals
                st.session_state['backlog'] = backlog
                #st.session_state['inventory'] = inventory


                ## output from function
                st.session_state['results0'] = results0
                st.session_state['results1'] = results1
                st.session_state['results2'] = results2
                st.session_state['results3'] = results3

                # update dataframe state
                #st.session_state['mydf'] = st.session_state.dff.append({'col 0': col1, 'col 1':col2}, ignore_index=True)


                # still empty as state is not persisted
                st.text("Updated dataframe")
                st.text(st.session_state['counter'])
                st.dataframe(st.session_state['results0'])

            else:
                st.text("End of Simulation")
                st.text(st.session_state['counter'])
                st.dataframe(st.session_state['results0'])
                iDISPLAY_FINAL_STATS = True



if iDISPLAY_FINAL_STATS == True:

    incoming_demand = st.session_state['incoming_demand']
    stocks = st.session_state['stocks']
    shipped_order = st.session_state['shipped_order']
    outgoing_order_arrival_schedule = st.session_state['outgoing_order_arrival_schedule']
    outgoing_order_arrival_actuals = st.session_state['outgoing_order_arrival_actuals']
    backlog = st.session_state['backlog']


    header_column_names = ['Retailer', 'Wholeseller', 'Distributor', 'Factory']

    pdf_EOQ_distribution = pd.DataFrame()
    pdf_INVENTORY_fluctuations = pd.DataFrame()

    for facility in range(0, len(cntfacility)):
        results_retailer = pd.DataFrame({
            "demanded": runtime_lstOflsts_incoming_demand[facility],
            "EOQed": runtime_lstOflsts_eoq_qty_decision[facility],
            "actual_arrivals": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
            "stocks_eop": stocks[facility],
            "backlogs_eop": backlog[facility],
            "Shipped_eop": shipped_order[facility]

            # "scheduled_arrivals_qty_bop": outgoing_order_arrival_schedule[0][0:len(stocks[0])],

        })

        INV_BO_Costs = (results_retailer['stocks_eop'] * storageOrHolding_cost_per_unit) + (
                    results_retailer['backlogs_eop'] * shortageOrEmergencyOrBackordered_cost_per_unit)
        INV_fluctuations = results_retailer['stocks_eop'] - results_retailer['backlogs_eop']

        # print(INV_BO_Costs.values.cumsum())
        pdf_EOQ_distribution[str(facility)] = results_retailer['EOQed'].values
        pdf_INVENTORY_fluctuations[str(facility)] = INV_fluctuations.values

    pdf_EOQ_distribution.columns = header_column_names
    pdf_INVENTORY_fluctuations.columns = header_column_names

    # PLOTTING
    plt.style.use('ggplot')

    # reset index and rename column as week
    # order distribution pdf
    pdf_EOQ_distribution = pdf_EOQ_distribution.reset_index()
    pdf_EOQ_distribution.rename(columns={'index': 'Week'}, inplace=True)

    # INVENTORY_fluctuations pdf
    pdf_INVENTORY_fluctuations = pdf_INVENTORY_fluctuations.reset_index()
    pdf_INVENTORY_fluctuations.rename(columns={'index': 'Week'}, inplace=True)

    # increment week by 1 to start from week-1
    pdf_EOQ_distribution['Week'] = pdf_EOQ_distribution['Week'] + 1
    pdf_INVENTORY_fluctuations['Week'] = pdf_INVENTORY_fluctuations['Week'] + 1

    st.text("\n")

    with st.container():
        # USER-INPUT SECTION - 2
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.subheader("EOQ Order Quantity Distribution")
            # # Plot-1
            # plt1 = pdf_EOQ_distribution.plot(x="Week", y=header_column_names)
            # #plt1.savefig("pdf_EOQ_distribution.png")
            # st.pyplot(plt1)
            x = pdf_EOQ_distribution['Week']
            y = pdf_EOQ_distribution[header_column_names]

            plt.figure()
            plt.plot(x, y)

            lines = plt.plot(x, y)

            plt.xlabel("time-weeks")
            plt.ylabel("Order (Quantity)")

            plt.title("EOQ Order Distribution")
            plt.legend(lines[:4], header_column_names, loc='upper left')
            st.pyplot(plt)


        with col2:
            st.subheader("Inventory Fluctuations")
            # # plot-2
            # plt2 = pdf_INVENTORY_fluctuations.plot(x="Week", y=header_column_names)
            # #plt2.savefig("pdf_INVENTORY_fluctuations.png")
            # st.pyplot(plt2)
            x = pdf_INVENTORY_fluctuations['Week']
            y = pdf_INVENTORY_fluctuations[header_column_names]
            plt.figure()
            # Plot a simple line chart
            #plt.plot(x, y, 'c', label='Portfolio')
            plt.plot(x, y)

            lines = plt.plot(x, y)

            plt.xlabel("time-weeks")
            plt.ylabel("Inventory (Quantity)")
            plt.title("Inventory Fluctuations")
            plt.legend(lines[:4], header_column_names,loc='upper left')
            st.pyplot(plt)


        with col3:
            st.subheader("EOQ Order-Distribution Summary")
            # summary-table
            pdf_EOQ_distribution.set_index("Week", inplace=True)
            pdf_summary = pdf_EOQ_distribution.describe()
            pdf_summary = pdf_summary.reset_index()
            st.dataframe(pdf_summary)

