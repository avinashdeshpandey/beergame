
# ENV py31013
# THIS IS dynamic tool:
# # python -m streamlit run 3_beergame_WIP.py
import os
import streamlit as st
import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm
import random
import matplotlib.pyplot as plt

random.seed(int(random.randint(1212152125162, 17283834994069956895)))

# eoq policy = demand*lead_time + backlog - Inventory

###################################################################################################################################
# USER PARAMETERS
##################################################################################################################################
IND_ALL_ECHELONS_COMMON_INFO = False
iDISPLAY_FINAL_STATS = False
iSESSION_VAR_INITIATED = False
iROLE = 0  # RETAILER, WHOLESELLER, DISTRIBUTOR, MANUFACTURER
number_of_turns = 11
# supplier_lead_time = [1,1,1,1] # -1 => same week / instantaneous delivery# LETS RUN FOR RETAILER:
# initial_stock = [15,15,15,15]
# initial_backlog = [0,0,0,0]
cntfacility = [1,1,1,1]  # each number reprsents count of each facility, from left to right; 1-retialer, 1-wholeseller, 1-distributor & 1-manufacturer
# COSTS
ordering_or_setup_cost_perorder = 5  ## K like setup octs
cost_per_unit = 15   # unit purchase cost
storageOrHolding_cost_per_unit = 0.5 # for every-item that is in unsold inventory
shortageOrEmergencyOrBackordered_cost_per_unit = 1 # placed end of week and delievered instantaaneously

URL_HOWTOUSE_IMAGES = "./images/"



###################################################################################################################################
# DO NOT CHANGE ANYTHING BELOW THIS
##################################################################################################################################
# #
# # MANUAL RUN - setting ---------START
# incoming_demand = [[], [], [], []]
# stocks = [[], [], [], []]
# shipped_order = [[], [], [], []]
# outgoing_order_arrival_schedule = []
# outgoing_order_arrival_actuals = []
# backlog = [[], [], [], []]
# inventory = [[], [], [], []]
# mydata = pd.DataFrame({"col 0": [],
#                        "col 1": []})
# counter = 0
# runtime_lstOflsts_incoming_demand = [[], [], [], []]
# runtime_lstOflsts_eoq_qty_decision = [[], [], [], []]
# lstoflsts_pendingorders_today_scheduled = [[], [], [], []]
# lstoflsts_pendingorders_today_actualarrived = [[], [], [], []]
#
# results0 = pd.DataFrame({"DEMAND": [],
#                          "ORDER_PLACED": [],
#                          "ORDER_ARRIVED(act)": [],
#                          "INVENTORY(eop)": [],
#                          "BACKLOGS(eop)": [],
#                          "SHIPPED(eop)": [],
#                          "PENDING_ARRIVALS(ttl)": []
#                          })
# results1 = pd.DataFrame({"DEMAND": [],
#                          "ORDER_PLACED": [],
#                          "ORDER_ARRIVED(act)": [],
#                          "INVENTORY(eop)": [],
#                          "BACKLOGS(eop)": [],
#                          "SHIPPED(eop)": [],
#                          "PENDING_ARRIVALS(ttl)": []
#                          })
# results2 = pd.DataFrame({"DEMAND": [],
#                          "ORDER_PLACED": [],
#                          "ORDER_ARRIVED(act)": [],
#                          "INVENTORY(eop)": [],
#                          "BACKLOGS(eop)": [],
#                          "SHIPPED(eop)": [],
#                          "PENDING_ARRIVALS(ttl)": []
#                          })
# results3 = pd.DataFrame({"DEMAND": [],
#                          "ORDER_PLACED": [],
#                          "ORDER_ARRIVED(act)": [],
#                          "INVENTORY(eop)": [],
#                          "BACKLOGS(eop)": [],
#                          "SHIPPED(eop)": [],
#                          "PENDING_ARRIVALS(ttl)": []
#                          })
# lst_eoq_ui = []
# ret_initial_stock = 15
# ret_initial_backlog = 0
# mu = 10
# sigma = 3
# order_arrival_leadtimes = 1
# supplier_lead_time = [order_arrival_leadtimes] * len(cntfacility)  # -1 => same week / instantaneous delivery# LETS RUN FOR RETAILER:
# initial_stock = [ret_initial_stock] * len(cntfacility)
# initial_backlog = [ret_initial_backlog] * len(cntfacility)
# user_eoq_qty = 0
#
# outgoing_order_arrival_schedule.append(
#     [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
# outgoing_order_arrival_schedule.append(
#     [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
# outgoing_order_arrival_schedule.append(
#     [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
# outgoing_order_arrival_schedule.append(
#     [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
#
# outgoing_order_arrival_actuals.append(
#     [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
# outgoing_order_arrival_actuals.append(
#     [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
# outgoing_order_arrival_actuals.append(
#     [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
# outgoing_order_arrival_actuals.append(
#     [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
#
#
#
# isim=counter
# current_user_role=iROLE
# user_eoq_qty = 25
# mu_sigma_eoq=[mu, sigma, user_eoq_qty]
# iINDUCE_ARRIVAL_QTYS_VARIABILITY=False
# iORDERGENMODE='Manual'
#
# # MANUAL RUN - setting ---------END


## Declare session varibles....
if "incoming_demand" not in st.session_state:
    incoming_demand = [[], [], [], []]
    st.session_state['incoming_demand'] = incoming_demand

if "stocks" not in st.session_state:
    stocks = [[], [], [], []]
    st.session_state['stocks'] = stocks

if "shipped_order" not in st.session_state:
    shipped_order = [[], [], [], []]
    st.session_state['shipped_order'] = shipped_order

if "outgoing_order_arrival_schedule" not in st.session_state:
    outgoing_order_arrival_schedule = []

    st.session_state['outgoing_order_arrival_schedule'] = outgoing_order_arrival_schedule

if "outgoing_order_arrival_actuals" not in st.session_state:
    outgoing_order_arrival_actuals = []
    st.session_state['outgoing_order_arrival_actuals'] = outgoing_order_arrival_actuals

if "backlog" not in st.session_state:
    backlog = [[], [], [], []]
    st.session_state['backlog'] = backlog

if "inventory" not in st.session_state:
    inventory = [[], [], [], []]
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

if "lstoflsts_pendingorders_today_scheduled" not in st.session_state:
    lstoflsts_pendingorders_today_scheduled = [[], [], [], []]
    st.session_state['lstoflsts_pendingorders_today_scheduled'] = lstoflsts_pendingorders_today_scheduled

if "lstoflsts_pendingorders_today_actualarrived" not in st.session_state:
    lstoflsts_pendingorders_today_actualarrived = [[], [], [], []]
    st.session_state['lstoflsts_pendingorders_today_actualarrived'] = lstoflsts_pendingorders_today_actualarrived


# persist state of dataframe
if "results0" not in st.session_state:
    results0 = pd.DataFrame({"DEMAND": [],
                             "ORDER_PLACED": [],
                             "ORDER_ARRIVED(act)": [],
                             "INVENTORY(eop)": [],
                             "BACKLOGS(eop)": [],
                             "SHIPPED(eop)": [],
                             "PENDING_ARRIVALS(ttl)":[]
                             })
    st.session_state['results0'] = results0

if "results1" not in st.session_state:
    results1 = pd.DataFrame({"DEMAND": [],
                             "ORDER_PLACED": [],
                             "ORDER_ARRIVED(act)": [],
                             "INVENTORY(eop)": [],
                             "BACKLOGS(eop)": [],
                             "SHIPPED(eop)": [],
                             "PENDING_ARRIVALS(ttl)":[]
                             })
    st.session_state['results1'] = results1

if "results2" not in st.session_state:
    results2 = pd.DataFrame({"DEMAND": [],
                             "ORDER_PLACED": [],
                             "ORDER_ARRIVED(act)": [],
                             "INVENTORY(eop)": [],
                             "BACKLOGS(eop)": [],
                             "SHIPPED(eop)": [],
                             "PENDING_ARRIVALS(ttl)":[]
                             })
    st.session_state['results2'] = results2

if "results3" not in st.session_state:
    results3 = pd.DataFrame({"DEMAND": [],
                             "ORDER_PLACED": [],
                             "ORDER_ARRIVED(act)": [],
                             "INVENTORY(eop)": [],
                             "BACKLOGS(eop)": [],
                             "SHIPPED(eop)": [],
                             "PENDING_ARRIVALS(ttl)":[]
                             })
    st.session_state['results3'] = results3

if "lst_eoq_ui" not in st.session_state:
    st.session_state['lst_eoq_ui'] = []

# mydata = st.session_state['mydata']
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

lstoflsts_pendingorders_today_scheduled = st.session_state['lstoflsts_pendingorders_today_scheduled']
lstoflsts_pendingorders_today_actualarrived = st.session_state['lstoflsts_pendingorders_today_actualarrived']


lst_eoq_ui = st.session_state['lst_eoq_ui']

results0 = st.session_state['results0']
results1 = st.session_state['results1']
results2 = st.session_state['results2']
results3 = st.session_state['results3']


## following objects will be required to track...scheduled EOQs vs whts actually delivered by upper echelon!

def fsimulatebeergame(isim,current_user_role,mu_sigma_eoq,iINDUCE_ARRIVAL_QTYS_VARIABILITY,iORDERGENMODE):
    """
    :param isim: time-period / run
    :param user_role: what role you are assuming
    :return: it updates runtime_lstOflsts_incoming_demand object
    mu_sigma_eoq = [10,3,5]
    """
    mu = int(mu_sigma_eoq[0])
    sigma = int(mu_sigma_eoq[1])
    user_ordered_eoq = int(mu_sigma_eoq[2])

    # iINDUCE_ARRIVAL_QTYS_VARIABILITY == False

    # loop through 1-facility at a time & create/update lstOflsts to store numbers
    for user_role in range(0, len(cntfacility)): ## for each facility get/generate demand & EOQs
        # for each
        if current_user_role == user_role:
            # GENERATE DEMAND:
            usergiven_or_generate_demand = int(random.normalvariate(mu, sigma))    # for hard values we can use >>> lstOflsts_incoming_demand[user_role][isim]
            # SAVE NUMBER
            runtime_lstOflsts_incoming_demand[user_role].append(usergiven_or_generate_demand)


            # naive_eoq = est_demand * int(supplier_lead_time[user_role]) - stocks[user_role][isim] - np.max([lstoflsts_pendingorders_today_scheduled[user_role][isim] - backlog[user_role][isim], 0])
            # usergiven_or_generate_demand = np.max([naive_eoq, 0])
            # # SAVE NUMBER
            # runtime_lstOflsts_incoming_demand[user_role].append(usergiven_or_generate_demand)

            # CALCULATE EOQ:  How much to order ? EOQ-decision ? this is a user input
            # EOQ = demand_LT * LeadTime + Inventory - Backlogs
            # usergiven_or_generate_eoq_decision = user_ordered_eoq  # for hard values we can use >>> lstOflsts_eoq_qty_decision[user_role][isim]
            # runtime_lstOflsts_eoq_qty_decision[user_role].append(usergiven_or_generate_eoq_decision)



            # CALCULATE stock-availability ? stocks[i-1] + incoming_deliveries (these are the actuals that we reeived )
            if isim == 0:
                actual_arrival = outgoing_order_arrival_schedule[user_role][isim]  ## this is given by user or function-generated value , here actual delivered could be reduced
                outgoing_order_arrival_actuals[user_role][isim] = actual_arrival  # lets update arrivals array

                # lets take a look at how many are pending-orders in the pipeline
                ## actuals_arrived <= scheduled_Arrivals
                pending_orders_scheduledarrivals_ason_isim_day = np.array(outgoing_order_arrival_schedule[user_role][isim + 1:]).sum()
                pending_orders_actualarrivals_ason_isim_day = np.array(outgoing_order_arrival_actuals[user_role][isim + 1:]).sum()
                lstoflsts_pendingorders_today_scheduled[user_role].append(pending_orders_scheduledarrivals_ason_isim_day)
                lstoflsts_pendingorders_today_actualarrived[user_role].append(pending_orders_actualarrivals_ason_isim_day)

                stock_available = initial_stock[user_role] + outgoing_order_arrival_actuals[user_role][isim]
                stocks[user_role].append(stock_available)
                # backorder
                backlog[user_role].append(initial_backlog[user_role])

                #generate_EOQ_to_order = np.max([stock_available,runtime_lstOflsts_incoming_demand[user_role],backlog[user_role]])

            else:
                # what is arriving-now..so that it can be used to fulfill order ?
                actual_arrival = outgoing_order_arrival_schedule[user_role][isim]   ## this is given by user or function-generated value
                outgoing_order_arrival_actuals[user_role][isim] = actual_arrival  # lets update arrivals array

                # let's take a look at how many are pending-orders in the pipeline
                ## actuals_arrived <= scheduled_Arrivals
                pending_orders_scheduledarrivals_ason_isim_day = np.array(outgoing_order_arrival_schedule[user_role][isim + 1:]).sum()
                pending_orders_actualarrivals_ason_isim_day = np.array(outgoing_order_arrival_actuals[user_role][isim + 1:]).sum()
                lstoflsts_pendingorders_today_scheduled[user_role].append(pending_orders_scheduledarrivals_ason_isim_day)
                lstoflsts_pendingorders_today_actualarrived[user_role].append(pending_orders_actualarrivals_ason_isim_day)

                # Inventory available from which demand can be FULFILLED is;
                stock_available = stocks[user_role][isim - 1] + outgoing_order_arrival_actuals[user_role][isim]
                # lets append this value
                stocks[user_role].append(stock_available)
                backlog[user_role].append(backlog[user_role][isim - 1])


            # when will this EOQ arrive ?..schduled & arriavls will be same ...no lead-time variability in the qty for now
            # # the lead-times are at least 1-week & therefoew it can be here below above section...
            # outgoing_order_arrival_schedule[user_role][isim + int(supplier_lead_time[user_role]) + 1] = usergiven_or_generate_eoq_decision
            # outgoing_order_arrival_actuals[user_role][isim + int(supplier_lead_time[user_role]) + 1] = usergiven_or_generate_eoq_decision

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


                if runtime_lstOflsts_incoming_demand[user_role][isim] > 0.0:
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


            # HOW MUCH TO ORDER ?
            usergiven_or_generate_eoq_decision = 0
            if iORDERGENMODE == 'Manual':
                usergiven_or_generate_eoq_decision = np.max([user_ordered_eoq, 0])

                # Lets save this generated EOQ for this entity
                runtime_lstOflsts_eoq_qty_decision[user_role].append(usergiven_or_generate_eoq_decision)

            elif iORDERGENMODE == 'Auto':
                # usergiven_or_generate_eoq_decision = np.max([stocks[user_role][isim],runtime_lstOflsts_incoming_demand[user_role][isim] * int(supplier_lead_time[user_role]), backlog[user_role][isim]])

                if backlog[user_role][isim] > 0:
                    usergiven_or_generate_eoq_decision = runtime_lstOflsts_incoming_demand[user_role][isim] * int(supplier_lead_time[user_role]) + np.max([backlog[user_role][isim] - stocks[user_role][isim], 0])

                if stocks[user_role][isim] > 0:
                    usergiven_or_generate_eoq_decision = np.max([runtime_lstOflsts_incoming_demand[user_role][isim] * int(supplier_lead_time[user_role]) - stocks[user_role][isim], 0])

                # Lets save this generated EOQ for this entity
                runtime_lstOflsts_eoq_qty_decision[user_role].append(usergiven_or_generate_eoq_decision)


            elif iORDERGENMODE == 'Naive':
                naive_eoq = runtime_lstOflsts_incoming_demand[user_role][isim] * int(supplier_lead_time[user_role]) - stocks[user_role][isim] - np.max([lstoflsts_pendingorders_today_scheduled[user_role][isim]-backlog[user_role][isim],0])
                #generate_EOQ_to_order = np.max([stocks[user_role][isim], runtime_lstOflsts_incoming_demand[user_role][isim], backlog[user_role][isim]])
                usergiven_or_generate_eoq_decision = np.max([naive_eoq,0])

                # Lets save this generated EOQ for this entity
                runtime_lstOflsts_eoq_qty_decision[user_role].append(usergiven_or_generate_eoq_decision)

            else:
                print("ERROR: iORDERGENMODE value has to Manual or Naive or Auto.")
                quit()

            # & WHEN will this EOQ order arrive ??? the lead-times are at least 1-week & therefoew it can be here below above section...
            outgoing_order_arrival_schedule[user_role][isim + int(supplier_lead_time[user_role]) + 1] = usergiven_or_generate_eoq_decision
            outgoing_order_arrival_actuals[user_role][isim + int(supplier_lead_time[user_role]) + 1] = usergiven_or_generate_eoq_decision


        elif current_user_role < user_role:
            # since the user is retailer....whatever retailer orders that will be wholeseller`s demand!
            # wholeseller - demand = EOQ from retailer
            # wholeseller - EOQ = function or given values
            iUSER_LOWER_ECHELON_ORDER_AS_DEMAND = True

            if iUSER_LOWER_ECHELON_ORDER_AS_DEMAND == True:
                # retailers-EOQ is wholeseller`s demand
                usergiven_or_generate_demand = runtime_lstOflsts_eoq_qty_decision[user_role-1][isim] # just get the user given value @ ith posiiton/isim
                usergiven_or_generate_demand = usergiven_or_generate_demand
                # save this value
                runtime_lstOflsts_incoming_demand[user_role].append(usergiven_or_generate_demand)
            else:
                # GENERATE DEMAND:
                usergiven_or_generate_demand = np.max(int(random.normalvariate(mu,sigma)), runtime_lstOflsts_eoq_qty_decision[user_role-1][isim])
                usergiven_or_generate_demand = usergiven_or_generate_demand
                # SAVE NUMBER
                runtime_lstOflsts_incoming_demand[user_role].append(usergiven_or_generate_demand)
                # use same customer-demand fundtion used by retailer


            # EOQ
            # CALCULATE EOQ:  How much to order EOQ-decision ? this is a user input
            # we are deciding EOQ-order at the EOP: naive estimate is EOQ = demand*lead-time + current-inventory + arrivals next-week - backlogs

            if isim == 0:
                actual_arrival = outgoing_order_arrival_schedule[user_role][isim]  ## this is given by user or function-generated value , here actual delivered could be reduced
                outgoing_order_arrival_actuals[user_role][isim] = actual_arrival  # lets update arrivals array

                # lets take a look at how many are pending-orders in the pipeline
                ## actuals_arrived <= scheduled_Arrivals
                pending_orders_scheduledarrivals_ason_isim_day = np.array(outgoing_order_arrival_schedule[user_role][isim + 1:]).sum()
                pending_orders_actualarrivals_ason_isim_day = np.array(outgoing_order_arrival_actuals[user_role][isim + 1:]).sum()
                lstoflsts_pendingorders_today_scheduled[user_role].append(pending_orders_scheduledarrivals_ason_isim_day)
                lstoflsts_pendingorders_today_actualarrived[user_role].append(pending_orders_actualarrivals_ason_isim_day)

                stock_available = initial_stock[user_role] + outgoing_order_arrival_actuals[user_role][isim]
                stocks[user_role].append(stock_available)
                # backorder
                backlog[user_role].append(initial_backlog[user_role])

            else:
                actual_arrival = outgoing_order_arrival_schedule[user_role][isim]   ## this is given by user or function-generated value
                outgoing_order_arrival_actuals[user_role][isim] = actual_arrival  # lets update arrivals array

                # lets take a look at how many are pending-orders in the pipeline
                ## actuals_arrived <= scheduled_Arrivals
                pending_orders_scheduledarrivals_ason_isim_day = np.array(outgoing_order_arrival_schedule[user_role][isim + 1:]).sum()
                pending_orders_actualarrivals_ason_isim_day = np.array(outgoing_order_arrival_actuals[user_role][isim + 1:]).sum()
                lstoflsts_pendingorders_today_scheduled[user_role].append(pending_orders_scheduledarrivals_ason_isim_day)
                lstoflsts_pendingorders_today_actualarrived[user_role].append(pending_orders_actualarrivals_ason_isim_day)

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
                backlog[user_role][isim] = backlog[user_role][isim - 1] + int(runtime_lstOflsts_incoming_demand[user_role][isim])
                shipped_order[user_role].append(0)

            else:
                print("ERROR LINE-147: stocks cannot be negative !!!")
                quit()


            # HOW MUCH TO ORDER ? this is by defauly Naive fornow
            generate_EOQ_to_order = 0
            if iORDERGENMODE == 'Naive':
                naive_eoq = runtime_lstOflsts_incoming_demand[user_role][isim] * int(supplier_lead_time[user_role]) - stocks[user_role][isim] - np.max([lstoflsts_pendingorders_today_scheduled[user_role][isim]-backlog[user_role][isim],0])
                generate_EOQ_to_order = np.max([naive_eoq,0])
                # Lets save this generated EOQ for this entity
                runtime_lstOflsts_eoq_qty_decision[user_role].append(generate_EOQ_to_order)

            elif iORDERGENMODE in ['Auto','Manual']:
                if backlog[user_role][isim] > 0:
                    generate_EOQ_to_order = runtime_lstOflsts_incoming_demand[user_role][isim] * int(supplier_lead_time[user_role]) + np.max([backlog[user_role][isim] - stocks[user_role][isim], 0])
                    # generate_EOQ_to_order = np.max([stocks[user_role][isim], runtime_lstOflsts_incoming_demand[user_role][isim] * int(supplier_lead_time[user_role]), backlog[user_role][isim]])

                if stocks[user_role][isim] > 0:
                    generate_EOQ_to_order = np.max([runtime_lstOflsts_incoming_demand[user_role][isim] * int(supplier_lead_time[user_role]) - stocks[user_role][isim], 0])

                # Lets save this generated EOQ for this entity
                runtime_lstOflsts_eoq_qty_decision[user_role].append(generate_EOQ_to_order)

            else:
                print("ERROR: non-user facility iORDERGENMODE value not found.")
                quit()



            # & WHEN will this EOQ order arrive ??? the lead-times are at least 1-week & therefoew it can be here below above section...
            outgoing_order_arrival_schedule[user_role][isim + int(supplier_lead_time[user_role]) + 1] = generate_EOQ_to_order
            outgoing_order_arrival_actuals[user_role][isim + int(supplier_lead_time[user_role]) + 1] = generate_EOQ_to_order


        else:
            print("ERROR line-402: facility not found")
            quit()


    facility = 0
    results0 = pd.DataFrame({
        "DEMAND": runtime_lstOflsts_incoming_demand[facility],
        "ORDER_PLACED": runtime_lstOflsts_eoq_qty_decision[facility],
        "ORDER_ARRIVED(act)": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
        "INVENTORY(eop)": stocks[facility],
        "BACKLOGS(eop)":backlog[facility],
        "SHIPPED(eop)": shipped_order[facility],
        "PENDING_ARRIVALS(ttl)": lstoflsts_pendingorders_today_scheduled[facility]
    })

    facility = 1
    results1 = pd.DataFrame({
        "DEMAND": runtime_lstOflsts_incoming_demand[facility],
        "ORDER_PLACED": runtime_lstOflsts_eoq_qty_decision[facility],
        "ORDER_ARRIVED(act)": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
        "INVENTORY(eop)": stocks[facility],
        "BACKLOGS(eop)":backlog[facility],
        "SHIPPED(eop)": shipped_order[facility],
        "PENDING_ARRIVALS(ttl)": lstoflsts_pendingorders_today_scheduled[facility]
    })

    facility = 2
    results2 = pd.DataFrame({
        "DEMAND": runtime_lstOflsts_incoming_demand[facility],
        "ORDER_PLACED": runtime_lstOflsts_eoq_qty_decision[facility],
        "ORDER_ARRIVED(act)": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
        "INVENTORY(eop)": stocks[facility],
        "BACKLOGS(eop)":backlog[facility],
        "SHIPPED(eop)": shipped_order[facility],
        "PENDING_ARRIVALS(ttl)": lstoflsts_pendingorders_today_scheduled[facility]
    })

    facility = 3
    results3 = pd.DataFrame({
        "DEMAND": runtime_lstOflsts_incoming_demand[facility],
        "ORDER_PLACED": runtime_lstOflsts_eoq_qty_decision[facility],
        "ORDER_ARRIVED(act)": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
        "INVENTORY(eop)": stocks[facility],
        "BACKLOGS(eop)":backlog[facility],
        "SHIPPED(eop)": shipped_order[facility],
        "PENDING_ARRIVALS(ttl)": lstoflsts_pendingorders_today_scheduled[facility]
    })


    return results0, results1, results2, results3



##################################################################################
# UI-BEGINS
################################################################################


st.set_page_config(layout="wide")
st.title("DEMONSTRATION: 'Bullwhip Effect'")
st.text("Bullwhip Effect = The demand order variabilities in the supply chain get amplified at higher-echelons of supply chain, .")
st.divider()
with st.container():
    tabapp, tabhowtouse = st.tabs(["The App","How to Use"])

    with tabapp:
        with st.container():
            seluserc1, seluserc2 = st.columns([0.2,0.8])
            with seluserc1:
                select_user_role = st.selectbox("Select your supply chain role",["","Retailer"])

        st.divider()
        if select_user_role in ["Retailer", "Wholeseller", "Distributor", "Manufacturer"]:

            #st.subheader("You are playing as  = 'RETAILER' ")
            st.text("\n")
            st.text("Set the Inventory Policy as " + select_user_role)
            # 4 tabs to get the demand setting inmformation for each entity
            if select_user_role == "Retailer":
                tabRET, tabhowitworks = st.tabs(["Retailer","How to use"]) #, "Wholeseller", "Distributor", "Manufacturer"])
                #tabRET, tabWSR, tabDBTR, tabMANU = st.tabs(["Retailer", "Wholeseller", "Distributor", "Manufacturer"])

                with tabRET:
                    st.write("Retailer: Inventory Policy Setting Parameters")
                    tabRETc1, tabRETc2, tabRETc3 = st.columns([0.4,0.4,1])
                    with tabRETc1:
                        #iROLE = 0 --definied at the top
                        # lets set the object-values that are not going to change during simulation run.
                        # lead-times more or less will be constant once set
                        # Initial inventory levels /backlogs  at each facility is a one time check/settings
                        # Even demand-function is a one-time input parameter at-times
                        # the only thing a user has to enter everytime is EOQ

                        # initialize session state variables
                        if "mean_demand" not in st.session_state:
                            st.session_state["mean_demand"] = 0

                        if "stdev_demand" not in st.session_state:
                            st.session_state["stdev_demand"] = 0

                        st.text("1) Demand Parameters:")
                        demand_dist = st.selectbox("Demand Distribution",['Manual','Normal Distribution','Constant'])

                        if demand_dist == 'Normal Distribution':
                            st.session_state["mean_demand"] = st.number_input("Mean", min_value=15.0)
                            st.session_state["stdev_demand"] = st.number_input("Std Deviation", min_value=3.0)

                        elif demand_dist == 'Manual':
                            st.session_state["mean_demand"] = st.number_input("Mean", min_value=15.0)
                            st.session_state["stdev_demand"] = st.number_input("Std Deviation", min_value=3.0)

                        elif demand_dist == 'Constant':
                            st.session_state["mean_demand"] = st.number_input("Mean", min_value=15.0)
                            st.session_state["stdev_demand"] = 0

                        else:
                            st.text("No Demand Distribution Policy set!")


                        st.text("2) Current Inventory Status")
                        ret_initial_stock = st.number_input("Current Inventory (Qty)", min_value=15.0)
                        ret_initial_backlog = st.number_input("Backlogs (Qty)", min_value=0.0)

                        st.text("3) Order Lead Time (weeks)")
                        order_arrival_leadtimes = st.number_input("Order-Lead-time (number of weeks)", min_value=1.0)

                        # lets assign these values to variables
                        mu = st.session_state["mean_demand"]
                        sigma = st.session_state["stdev_demand"]
                        supplier_lead_time = [order_arrival_leadtimes] * len(cntfacility)  # -1 => same week / instantaneous delivery# LETS RUN FOR RETAILER:
                        initial_stock = [ret_initial_stock] * len(cntfacility)
                        initial_backlog = [ret_initial_backlog] * len(cntfacility)

                    with tabRETc2:
                        st.text("4) Place-Order (Decision-variable)")
                        user_eoq_qty = st.number_input("Purchase Order (Qty)", min_value=0.0)
                        st.text("NOTE: this EOQ order has default arrival lead time = 1-week, i.e if you order in say 1st week, the order will arrive starting 3rd week")

                        st.text("\n")
                        st.text("5) Simulation-Run Mode")
                        similation_scheme = st.selectbox("", ['','Manual','Auto'])

                    with tabRETc3:
                        st.text("Current inventory/backlog status, used to decide ORDER-QUANTITY under MANUAL-run mode.")
                        # Lets update some session - state variables which we have already initiated, based on user input

                        if st.session_state['counter']==0:
                            outgoing_order_arrival_schedule.append(
                                [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
                            outgoing_order_arrival_schedule.append(
                                [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
                            outgoing_order_arrival_schedule.append(
                                [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
                            outgoing_order_arrival_schedule.append(
                                [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))

                            outgoing_order_arrival_actuals.append(
                                [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
                            outgoing_order_arrival_actuals.append(
                                [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
                            outgoing_order_arrival_actuals.append(
                                [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))
                            outgoing_order_arrival_actuals.append(
                                [0] * (number_of_turns + int(supplier_lead_time[0]) + 1))

                        if similation_scheme == 'Manual':
                            # st.write("When you press the following button, the simulation will use the current parameter values to run the simulation.")
                            # st.write("you can change the demand, EOQ values depending upon your current week inventory/demand/backlog status.")

                            if st.button("Simulate for this week"):
                                if counter < number_of_turns:
                                    results0, results1, results2, results3 = fsimulatebeergame(isim = counter, current_user_role = iROLE, mu_sigma_eoq=[mu,sigma,user_eoq_qty],iINDUCE_ARRIVAL_QTYS_VARIABILITY=False, iORDERGENMODE=similation_scheme)

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

                        if similation_scheme == 'Auto':
                            st.write("Once you Press the followwing button, the simulation will run for " + str(number_of_turns) + " time-units & display final results at the bottom")
                            if st.button("Simulate for this week"):
                                for counter in range(0,number_of_turns):
                                    results0, results1, results2, results3 = fsimulatebeergame(isim = counter, current_user_role = iROLE, mu_sigma_eoq=[mu,sigma,user_eoq_qty],iINDUCE_ARRIVAL_QTYS_VARIABILITY=False,iORDERGENMODE=similation_scheme)

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

                                    if counter == number_of_turns - 1:
                                        iDISPLAY_FINAL_STATS = True


            else:
                st.write("Please select a user role")
                quit()

            st.divider()

            if iDISPLAY_FINAL_STATS == True:
                st.write("Final Simulation Results")
                incoming_demand = st.session_state['incoming_demand']
                stocks = st.session_state['stocks']
                shipped_order = st.session_state['shipped_order']
                outgoing_order_arrival_schedule = st.session_state['outgoing_order_arrival_schedule']
                outgoing_order_arrival_actuals = st.session_state['outgoing_order_arrival_actuals']
                backlog = st.session_state['backlog']


                header_column_names = ['Retailer', 'Wholeseller', 'Distributor', 'Factory']

                pdf_EOQ_distribution = pd.DataFrame()
                pdf_INVENTORY_fluctuations = pd.DataFrame()
                pdf_demand_distributions = pd.DataFrame()

                for facility in range(0, len(cntfacility)):
                    results_retailer = pd.DataFrame({
                        "DEMAND": np.array(runtime_lstOflsts_incoming_demand[facility]),
                        "ORDER_PLACED": np.array(runtime_lstOflsts_eoq_qty_decision[facility]),
                        "ORDER_ARRIVED(act)": np.array(outgoing_order_arrival_actuals[facility][0:len(stocks[facility])]),
                        "INVENTORY(eop)": np.array(stocks[facility]),
                        "BACKLOGS(eop)": np.array(backlog[facility]),
                        "SHIPPED(eop)": np.array(shipped_order[facility]),
                        "PENDING_ARRIVALS(ttl)": np.array(lstoflsts_pendingorders_today_scheduled[facility])
                    })

                    INV_BO_Costs = (results_retailer['INVENTORY(eop)'] * storageOrHolding_cost_per_unit) + (
                                results_retailer['BACKLOGS(eop)'] * shortageOrEmergencyOrBackordered_cost_per_unit)
                    INV_fluctuations = results_retailer['INVENTORY(eop)'] - results_retailer['BACKLOGS(eop)']

                    # print(INV_BO_Costs.values.cumsum())
                    pdf_EOQ_distribution[str(facility)] = results_retailer['ORDER_PLACED'].values
                    pdf_INVENTORY_fluctuations[str(facility)] = INV_fluctuations.values
                    pdf_demand_distributions[str(facility)] = results_retailer['DEMAND'].values

                pdf_EOQ_distribution.columns = header_column_names
                pdf_INVENTORY_fluctuations.columns = header_column_names
                pdf_demand_distributions.columns = header_column_names

                # PLOTTING
                plt.style.use('ggplot')

                # reset index and rename column as week
                # order distribution pdf
                pdf_EOQ_distribution = pdf_EOQ_distribution.reset_index()
                pdf_EOQ_distribution.rename(columns={'index': 'Week'}, inplace=True)

                # INVENTORY_fluctuations pdf
                pdf_INVENTORY_fluctuations = pdf_INVENTORY_fluctuations.reset_index()
                pdf_INVENTORY_fluctuations.rename(columns={'index': 'Week'}, inplace=True)

                # demand pdf
                # order distribution pdf
                pdf_demand_distributions = pdf_demand_distributions.reset_index()
                pdf_demand_distributions.rename(columns={'index': 'Week'}, inplace=True)


                # increment week by 1 to start from week-1
                pdf_EOQ_distribution['Week'] = pdf_EOQ_distribution['Week'] + 1
                pdf_INVENTORY_fluctuations['Week'] = pdf_INVENTORY_fluctuations['Week'] + 1
                pdf_demand_distributions['Week'] = pdf_demand_distributions['Week'] + 1

                st.text("\n")

                with st.container():
                    st.subheader("ORDER-QTY: SUMMARY")
                    colr1c1, colr1c2 = st.columns([1, 1])
                    with colr1c1:
                        x = pdf_EOQ_distribution['Week']
                        y = pdf_EOQ_distribution[header_column_names]
                        plt.figure()
                        plt.plot(x, y)
                        lines = plt.plot(x, y)
                        plt.xlabel("time-weeks")
                        plt.ylabel("Order(Qty)")
                        plt.title("ORDER-QTY: ALL ECHELONS")
                        plt.legend(lines[:4], header_column_names, loc='upper left')
                        st.pyplot(plt)

                    with colr1c2:

                        st.write("ORDER-QTY: Summary Statistics")
                        st.write("Bullwhip effect >>> verify increasing standard-deviation values, as you go up the echelon!")
                        # summary-table
                        pdf_EOQ_distribution.set_index("Week", inplace=True)
                        pdf_summary = pdf_EOQ_distribution.describe()
                        pdf_summary = pdf_summary.reset_index()
                        st.dataframe(pdf_summary)


                with st.container():
                    st.subheader("DEMAND: SUMMARY")
                    colr1c1, colr1c2 = st.columns([1, 1])
                    with colr1c1:
                        x = pdf_demand_distributions['Week']
                        y = pdf_demand_distributions[header_column_names]
                        plt.figure()
                        plt.plot(x, y)
                        lines = plt.plot(x, y)
                        plt.xlabel("time-weeks")
                        plt.ylabel("Demand(Qty)")
                        plt.title("DEMAND-QTY: ALL ECHELONS")
                        plt.legend(lines[:4], header_column_names, loc='upper left')
                        st.pyplot(plt)

                    with colr1c2:

                        st.write("DEMAND-QTY: Summary Statistics")
                        st.write("Bullwhip effect >>> verify increasing mean-demand values, as you go up the echelon!")
                        # summary-table
                        pdf_demand_distributions.set_index("Week", inplace=True)
                        pdf_summary2 = pdf_demand_distributions.describe()
                        pdf_summary2 = pdf_summary2.reset_index()
                        st.dataframe(pdf_summary2)

                st.divider()
                with st.container():
                    st.subheader("INVENTORY: SUMMARY")
                    colr1c1, colr1c2 = st.columns([1, 1])
                    with colr1c1:
                        x = pdf_INVENTORY_fluctuations['Week']
                        y = pdf_INVENTORY_fluctuations[header_column_names]
                        plt.figure()
                        plt.plot(x, y)
                        lines = plt.plot(x, y)
                        plt.xlabel("time-weeks")
                        plt.ylabel("Inventory(Qty)")
                        plt.title("INVENTORY: ALL ECHELONS")
                        plt.legend(lines[:4], header_column_names, loc='upper left')
                        st.pyplot(plt)

                    with colr1c2:

                        st.write("INVENTORY: Summary Statistics")
                        st.write("Bullwhip effect >>> verify increasing mean-demand values, as you go up the echelon!")
                        # summary-table
                        pdf_INVENTORY_fluctuations.set_index("Week", inplace=True)
                        pdf_summary3 = pdf_INVENTORY_fluctuations.describe()
                        pdf_summary3 = pdf_summary3.reset_index()
                        st.dataframe(pdf_summary3)


    with tabhowtouse:
        with st.container():
            tabhowtouser1c1, tabhowtouser1c2 = st.columns([1,1])

            with tabhowtouser1c1:
                st.write("What is this App about?")
                st.write("The is a simulation designed to demonstrate 'Bullwhip effect' across 4-level supply chain that consist of a RETAILER > a WHOLESELLER > a DISTRIBUTOR > a MANUFACTURER.")
                st.write("You will PLAY as a 'RETAILER' & the values for other levels will be generated by computer automatically during each run.")

            with tabhowtouser1c2:
                st.write("What is a 'Bullwhip effect'? ")
                st.write("It demonstrates, due to lack of information sharing amongsts supply chain participants, how actions at one stage of the supply chain can have significant impacts up the supply chain stages.")
                st.write("In particular, it shows;")
                st.write("1) Amplification of variability in demand as you move up the supply chain from retailers to manufacturers.")
                st.write("2) Discrepancies between inventory produced and demand.")
                st.write("3) Leading to excess inventory, lost revenue, and overinvestments.")


        st.divider()
        st.subheader("An Example to demonstrate application use and bullwhip effect interpretation using output.")
        st.divider()
        with st.container():
            tabhowtouser2c1, tabhowtouser2c2 = st.columns([1,1])

            with tabhowtouser2c1:
                st.image(URL_HOWTOUSE_IMAGES + '1_screen.png', caption='')

            with tabhowtouser2c2:
                st.write("This is the very 1st screen you will see when you open the app.")
                st.write("It has 2-tabs, 1) The App & 2) How to Use")
                st.write("By Default; you will see the tab-1) The App active.")


        st.divider()
        with st.container():
            tabhowtouser3c1, tabhowtouser3c2 = st.columns([1,1])

            with tabhowtouser3c1:
                st.image(URL_HOWTOUSE_IMAGES + '2_screen.png', caption='')


            with tabhowtouser3c2:
                st.write("Under The App tab, from the dropdown select 'Retailer', & you will see a new window with 2-tabs. The details explained next.")

        st.divider()
        with st.container():
            tabhowtouser4c1, tabhowtouser4c2 = st.columns([1,1])

            with tabhowtouser4c1:
                st.image(URL_HOWTOUSE_IMAGES + '3_screen.png', caption='')


            with tabhowtouser4c2:
                st.write("Here, as a Retailer, you will set Inventory Policy Settings values.'")
                st.write("Lets take a look at each of this section 1-at-a-time next")


        st.divider()
        with st.container():
            tabhowtouser5c0, tabhowtouser5c1, tabhowtouser5c2 = st.columns([0.2,1,1])

            with tabhowtouser5c0:
                st.write("USER-INPUT-1")

            with tabhowtouser5c1:
                st.image(URL_HOWTOUSE_IMAGES + '3_screen_1.png', caption='')

            with tabhowtouser5c2:
                st.write("1) Demand Information")
                st.write("This is customer-incoming demand distribution values. Enter mean & standard deviation in your case or you can retain default values.")

                st.write("2) Current Inventory Status information")
                st.write("Current Available Inventory, Any Current Backlogs or just retain default values.")

                st.write("3) Order Lead-times information")
                st.write("the default 1-implies that, when a order is placed, it takes 1 week & it will arrive begining of 2nd week.")

        st.divider()
        with st.container():
            tabhowtouser6c0, tabhowtouser6c1, tabhowtouser6c2 = st.columns([0.2,1,1])

            with tabhowtouser6c0:
                st.write("USER-INPUT-2")

            with tabhowtouser6c1:
                st.image(URL_HOWTOUSE_IMAGES + '3_screen_2.png', caption='')

            with tabhowtouser6c2:
                st.write("4) Order to be placed information")
                st.write("Decision variable: This is a order-quantity that you have to decide & enter manually")

                st.write("5) Simulation-Run Mode")
                st.write("we have 2-modes. Manual & Auto. Lets go through Manual-Mode in detail.")
                st.write("Mode-1 >>> its 'Manual' & in this mode, you run 1-simulation at a time (total 11-times for now), everyt-time having an option to change the Place-order (section 4 above).")
                st.write(
                    "Mode-2 >>> its 'Auto' & in this mode, you enter values only once and once you press 'Simulate', it will run 11-times automatically at the backend and will just produce final results.")

        st.divider()
        st.subheader("Mode-1  = 'Manual' >>> how to run steps as follows;")
        st.divider()
        with st.container():
            tabhowtouser6c2_r2c0, tabhowtouser6c2_r2c1, tabhowtouser6c2_r2c2 = st.columns([0.3, 1, 1])

            with tabhowtouser6c2_r2c0:
                st.subheader("1")

            with tabhowtouser6c2_r2c1:
                st.image(URL_HOWTOUSE_IMAGES + '3_screen_4.png', caption='')

            with tabhowtouser6c2_r2c2:
                st.write("Enter value for 'Place-order'. we entered 15 (you can enter any value you want)")

        st.divider()
        with st.container():
            tabhowtouser6c2_r3c0, tabhowtouser6c2_r3c1, tabhowtouser6c2_r3c2 = st.columns([0.3, 1, 1])

            with tabhowtouser6c2_r3c0:
                st.subheader("2")

            with tabhowtouser6c2_r3c1:
                st.image(URL_HOWTOUSE_IMAGES + '3_screen_5.png', caption='')

            with tabhowtouser6c2_r3c2:
                st.write("PRESS button 'simulate for this week'.")
                st.write("The output is a table as follows;")

        st.divider()
        with st.container():
            tabhowtouser6c2_r4c0, tabhowtouser6c2_r4c1, tabhowtouser6c2_r4c2 = st.columns([0.3, 1, 1])

            with tabhowtouser6c2_r4c0:
                st.subheader("3")

            with tabhowtouser6c2_r4c1:
                st.image(URL_HOWTOUSE_IMAGES + '3_screen_6.png', caption='')

            with tabhowtouser6c2_r4c2:
                st.write("Output: Statistics post 1st-simulation run under 'Manual-Mode'")
                st.write("DEMAND = customer demand generated using mean & standard-deviation given under section-1.")
                st.write("ORDER_PLACED = in step-1) the value you entered under section-4.")
                st.write("ORDER_ARRIVED = Any orders previously placed that arrived this week ( as we noted, every-order you place in 'order-placed' (section-4) arrives after the given lead-time).")
                st.write("INVENTORY(eop) = This is the Inventory status END-OF-WEEK that week after fulfilling any backlogs from previous week & incoming demand this week.")
                st.write("BACKLOGS(eop) = If the incoming demand cannot be fulfilled from existing INVENTORY, then it is BACKLOGGED.")
                st.write("SHIPPED(eop) = total Shipped quantity end of the week.")
                st.write("PENDING_ARRIVALS = this is the Order-due total quantity(orders yet to arrive totals) as of end of the week this week.")


        st.divider()
        with st.container():
            tabhowtouser6c2_r5c0, tabhowtouser6c2_r5c1, tabhowtouser6c2_r5c2 = st.columns([0.3, 1, 1])

            with tabhowtouser6c2_r5c0:
                st.subheader("4")

            with tabhowtouser6c2_r5c1:
                st.write("repeat 1 & 2 steps marked above in that order i.e;")
                st.write("1 - ENTER 'Place-Order' value (any quantity that you think is a proper order based on INVENTORY & BACKLOGS & DEMAND FUNCTION ")
                st.write("2 - PRESS 'simulate for this week'.")
                st.write("After repeating this 11-times, you will obtain result-table shown here & final 3-outputs (explained next)")


            with tabhowtouser6c2_r5c2:
                st.image(URL_HOWTOUSE_IMAGES + '3_screen_9.png', caption='')


        st.divider()
        st.subheader("Final output: Post simulation runs, following 3-outputs: each with a plot & summary-measures, can be used to analyze BULLWHIP EFFECT.")
        st.divider()
        with st.container():
            outpu1_c1, outpu1_c2 = st.columns([0.2, 1])
            with outpu1_c2:
                st.write("Output-1: Order-Placed (Qtys) across echelons and summary statistics with interpretation.")
                st.image(URL_HOWTOUSE_IMAGES + 'output1.png', caption='')

        st.divider()
        with st.container():
            outpu2_c1, outpu2_c2 = st.columns([0.2, 1])
            with outpu2_c2:
                st.write("Output-2: Demand-quantities (incoming) at each echelon and summary statistics with interpretation.")
                st.image(URL_HOWTOUSE_IMAGES + 'output2.png', caption='')

        st.divider()
        with st.container():
            outpu3_c1, outpu3_c2 = st.columns([0.2, 1])
            with outpu3_c2:
                st.write("Output-3: Inventory-levels at each echelon and summary statistics with interpretation.")
                st.image(URL_HOWTOUSE_IMAGES + 'output3.png', caption='')











# # ### FOR MANUAL TESTING--BEGINS
# for counter in range(0, number_of_turns):
#     results0, results1, results2, results3 = fsimulatebeergame(isim=counter, current_user_role=iROLE,
#                                                                mu_sigma_eoq=[mu, sigma, user_eoq_qty],
#                                                                iINDUCE_ARRIVAL_QTYS_VARIABILITY=False, iORDERGENMODE='Auto')
#
#     # increment counter
#     counter = counter + 1
#
# header_column_names = ['Retailer', 'Wholeseller', 'Distributor', 'Factory']
#
# pdf_EOQ_distribution = pd.DataFrame()
# pdf_INVENTORY_fluctuations = pd.DataFrame()
#
# for facility in range(0, len(cntfacility)):
#     results_retailer = pd.DataFrame({
#         "DEMAND": runtime_lstOflsts_incoming_demand[facility],
#         "ORDER_PLACED": runtime_lstOflsts_eoq_qty_decision[facility],
#         "ORDER_ARRIVED(act)": outgoing_order_arrival_actuals[facility][0:len(stocks[facility])],
#         "INVENTORY(eop)": stocks[facility],
#         "BACKLOGS(eop)": backlog[facility],
#         "SHIPPED(eop)": shipped_order[facility],
#         "PENDING_ARRIVALS(ttl)": lstoflsts_pendingorders_today_scheduled[facility]
#     })
#
#     INV_BO_Costs = (results_retailer['INVENTORY(eop)'] * storageOrHolding_cost_per_unit) + (
#             results_retailer['BACKLOGS(eop)'] * shortageOrEmergencyOrBackordered_cost_per_unit)
#     INV_fluctuations = results_retailer['INVENTORY(eop)'] - results_retailer['BACKLOGS(eop)']
#
#     # print(INV_BO_Costs.values.cumsum())
#     pdf_EOQ_distribution[str(facility)] = results_retailer['ORDER_PLACED'].values
#     pdf_INVENTORY_fluctuations[str(facility)] = INV_fluctuations.values
#
# pdf_EOQ_distribution.columns = header_column_names
# pdf_INVENTORY_fluctuations.columns = header_column_names
#
# # reset index and rename column as week
# # order distribution pdf
# pdf_EOQ_distribution = pdf_EOQ_distribution.reset_index()
# pdf_EOQ_distribution.rename(columns={'index': 'Week'}, inplace=True)
#
# # INVENTORY_fluctuations pdf
# pdf_INVENTORY_fluctuations = pdf_INVENTORY_fluctuations.reset_index()
# pdf_INVENTORY_fluctuations.rename(columns={'index': 'Week'}, inplace=True)
#
# # increment week by 1 to start from week-1
# pdf_EOQ_distribution['Week'] = pdf_EOQ_distribution['Week'] + 1
# pdf_INVENTORY_fluctuations['Week'] = pdf_INVENTORY_fluctuations['Week'] + 1
#
# ### FOR MANUAL TESTING--ENDS