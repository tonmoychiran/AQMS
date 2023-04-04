from django.shortcuts import render
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from .models import Finaldata
from django.db import connection
import pandas as pd
from json import load

def pm25data(divisionname):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT pm25 FROM finaldata WHERE division= %s ORDER BY rec_date desc limit 1", params=[divisionname])
    r = cursor.fetchone()

    return r[0]


def barchart(divisionname):

    cursor = connection.cursor()

    query = "SELECT YEAR(rec_date), AVG(pm25) FROM finaldata WHERE division=%s GROUP BY YEAR(rec_date)"

    df = pd.read_sql(query, connection, params=[divisionname])
    df.columns = ['year', 'pm25']
    fig = px.bar(
        data_frame=df, y=df["pm25"], x=df["year"], color='year', title="Yearly Average")
    return fig.to_html()

    #diction={ 'barchart': chart }

    #return render(request, 'index.html', context=diction)


def linechar(divisionname):
    cursor = connection.cursor()

    query1 = "select rec_date, pm25 from finaldata where division=%s"
    query2 = "select monthname(rec_date) as monthname, avg(pm25) as avgpm25 from finaldata where division=%s group by monthname(rec_date)"
    query3 = "SELECT YEAR(rec_date), AVG(pm25) FROM finaldata WHERE division=%s GROUP BY YEAR(rec_date)"

    df1 = pd.read_sql(query1, connection, params=[divisionname])
    df2 = pd.read_sql(query2, connection, params=[divisionname])
    df3 = pd.read_sql(query3, connection, params=[divisionname])

    df1.columns = ['date', 'pm25']
    #df2.columns = ['month', 'avgpm25']
    df3.columns = ['year', 'yravg']

    fig = go.Figure(data=[go.Line(
        name='daily',
        x=df1["date"],
        y=df1["pm25"],
        line=dict(
            color ='orange'
        )

    ),
        go.Line(
        name='monthly',
        x=df2["monthname"],
        y=df2["avgpm25"],
        line=dict(
            color='green'
        )
    ),
        go.Line(
        name="yearly",
        x=df3["year"],
        y=df3["yravg"],
        line=dict(
            color='blue'
    ))])

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Time: Daily",
                         method="update",
                         args=[{"visible": [True, False, False]},
                               {"title": "Daily pm2.5 data"}]),
                    dict(label="Time: Monthly",
                         method="update",
                         args=[{"visible": [False, True, False]},
                               {"title": "Monthly pm2.5 data",
                                }]),
                    dict(label="Time: Yearly",
                         method="update",
                         args=[{"visible": [False, False, True]},
                               {"title": "Yearly pm2.5 data"}])

                ]),
            )
        ])

    #fig=px.line( data_frame= df, y=df["pm25"], x= df["date"], title="Time Interval Data")
    #fig.update_xaxes(type='category')
    return fig.to_html()

    #diction={ 'linechart': chart }

    #return render(request, 'index.html', context=diction)


def seasonwise(divisionname):
    cursor = connection.cursor()

    query = "select season, pm25 from finaldata where division=%s"
    # query2= "SELECT season, pm25 AS pm254summer FROM finaldata WHERE division=%s AND season='summer'"
    # query3= "SELECT season, pm25 AS pm254autumn FROM finaldata WHERE division=%s AND season='autumn'"
    # query4= "SELECT season, pm25 AS pm254winter FROM finaldata WHERE division=%s AND season='winter'"
    # query5= "SELECT season, pm25 AS pm254spring FROM finaldata WHERE division=%s AND season='spring'"
    df = pd.read_sql(query, connection, params=[divisionname])
    # df2= pd.read_sql(query2, connection,params=[divisionname])
    # df3= pd.read_sql(query3, connection,params=[divisionname])
    # df4= pd.read_sql(query4, connection,params=[divisionname])
    # df5= pd.read_sql(query5, connection,params=[divisionname])

    # fig=go.Figure(data=[go.Box(
    #     name='All Season',
    #     x0=df["season"],
    #     y=df["pm25"]
    # ),
    # go.Box(
    #     name='Summer',
    #     x0=df2["season"],
    #     y=df2["pm254summer"]
    # ),
    # go.Box(
    #     name='Autumn',
    #     x0=df3["season"],
    #     y=df3["pm254autumn"]
    # ),
    # go.Box(
    #     name='Winter',
    #     x0=df4["season"],
    #     y=df4["pm254winter"],
    # ),
    # go.Box(
    #     name='Spring',
    #     x0=df5["season"],
    #     y=df5["pm254spring"],
    # )
    
    # ])

    # fig.update_layout(
    #     updatemenus=[dict(
    #         active=0,
    #         buttons=list([
    #         dict(label="Season: All",
    #                      method="update",
    #                      args=[{"visible": [True, False, False, False, False]},
    #                            {"title": "All Season pm25"}]),        
    #         dict(label="Season: Summer",
    #                      method="update",
    #                      args=[{"visible": [False, True, False, False, False]},
    #                            {"title": "Summer pm2.5"}]),
    #         dict(label="Season: Autumn",
    #                      method="update",
    #                      args=[{"visible": [False, False, True, False, False]},
    #                            {"title": "Autumn pm2.5"}]),
    #         dict(label="Season: Winter",
    #                      method="update",
    #                      args=[{"visible": [False, False, False, True, False]},
    #                            {"title": "Winter"}]),
    #         dict(label="Season: Spring",
    #                      method="update",
    #                      args=[{"visible": [False, False, False, False,True]},
    #                            {"title": "Spring pm25"}]),





    #         ])

    #     )   
        
    # ])


    fig = px.box(data_frame=df, y=df["pm25"], x=df["season"],
                 color='season', title="Season Wise Data")
    return fig.to_html()


def stationwise(divisionname):
    cursor = connection.cursor()

    query = "SELECT station AS st, AVG(pm25) AS avr FROM finaldata WHERE division=%s GROUP BY station ORDER BY station"

    df = pd.read_sql(query, connection, params=[divisionname])
    fig = px.box(data_frame=df, y=df["avr"], x=df["st"],
                 color='st', title="Station Wise Data")
    fig.update_xaxes(type='category')
    return fig.to_html()


def orgnwise(divisionname):
    cursor = connection.cursor()

    query = "SELECT rec_date,org_name, pm25 FROM finaldata WHERE division=%s"

    df = pd.read_sql(query, connection, params=[divisionname])
    fig = px.line(data_frame=df, x=df['rec_date'],
                  y=df['pm25'], color='org_name', title="Source Wise Data")
    #fig.update_xaxes(type='category')
    return fig.to_html()


def orgwisescatter(divisionname):
    cursor = connection.cursor()

    query = "SELECT rec_date,org_name, pm25 FROM finaldata WHERE division=%s"

    df = pd.read_sql(query, connection, params=[divisionname])
    fig = px.scatter(data_frame=df, x=df['rec_date'],
                     y=df['pm25'], color='org_name', title="Source Wise Data")  # , trendline="ols")
    return fig.to_html()


def home(request):
    cursor = connection.cursor()

    query = "select pm25, division from finaldata where rec_date in (select max(rec_date) from finaldata   group by division) order by division"
    df = pd.read_sql(query, connection)
    id = [0,1,2,3,4,5,6,7]
    df['id'] = id

    bd_divs = load(open('aqms/bangladesh_geojson_adm1_8_divisions_bibhags.json', 'r'))
    
    
    fig = px.choropleth(
    df,
    locations='id',
    geojson=bd_divs,
    color='pm25',
    hover_name='division',
    hover_data=['pm25'],
    color_continuous_scale=[[0.0, "green"], [0.10, "green"], [0.10, "yellow"], [0.20, "yellow"], [0.20, "orange"],[
        0.30, "orange"], [0.30, "red"],[0.40, "red"],[0.40, "purple"],[0.60, "purple"], [0.60, 'rgb(165, 0, 33)'],[1.0, 'rgb(165, 0, 33)']],
    range_color=[0, 500],
    

    )
    fig.update_geos(fitbounds="locations", visible=True, 
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar=dict(
        title="PM2.5",
        tickvals=[25,75,125,175,250,400],
        ticktext=["Good","Moderate","Unhealthy For Sensetive Groups","Unhealthy","Very Unhealthy","Hazardous"],
        lenmode="pixels", len=400,
    ), height=1000, width=1500,
    )

    figline = px.line(data_frame=df, x=df['division'],
                  y=df['pm25'])

    map=fig.to_html()
    line=figline.to_html()
    diction = {"map": map, "line": line}
    return render(request, 'dsh.html', context=diction)


def dhaka(request):
    divisionname = "Dhaka"
    diction = {"pmdata": pm25data(divisionname), "linechart": linechar(divisionname),  "boxplotchart": seasonwise(
        divisionname), "barchart": barchart(divisionname), "stationwiseboxplot": stationwise(divisionname), 'organization': orgnwise(divisionname), 'orgscatt': orgwisescatter(divisionname)}

    return render(request, 'dhakadash.html', context=diction)


def rangpur(request):
    divisionname = "Rangpur"
    diction = {"pmdata": pm25data(divisionname), "linechart": linechar(divisionname),  "boxplotchart": seasonwise(
        divisionname), "barchart": barchart(divisionname), "stationwiseboxplot": stationwise(divisionname), 'organization': orgnwise(divisionname), 'orgscatt': orgwisescatter(divisionname)}

    return render(request, 'rangpurdash.html', context=diction)


def khulna(request):
    divisionname = "Khulna"
    diction = {"pmdata": pm25data(divisionname), "linechart": linechar(divisionname),  "boxplotchart": seasonwise(
        divisionname), "barchart": barchart(divisionname), "stationwiseboxplot": stationwise(divisionname), 'organization': orgnwise(divisionname), 'orgscatt': orgwisescatter(divisionname)}

    return render(request, 'khulnadash.html', context=diction)


def sylhet(request):
    divisionname = "Sylhet"
    diction = {"pmdata": pm25data(divisionname), "linechart": linechar(divisionname),  "boxplotchart": seasonwise(
        divisionname), "barchart": barchart(divisionname), "stationwiseboxplot": stationwise(divisionname), 'organization': orgnwise(divisionname), 'orgscatt': orgwisescatter(divisionname)}

    return render(request, 'sylhetdash.html', context=diction)


def rajshahi(request):
    divisionname = "Rajshahi"
    diction = {"pmdata": pm25data(divisionname), "linechart": linechar(divisionname),  "boxplotchart": seasonwise(
        divisionname), "barchart": barchart(divisionname), "stationwiseboxplot": stationwise(divisionname), 'organization': orgnwise(divisionname), 'orgscatt': orgwisescatter(divisionname)}

    return render(request, 'rajshahidash.html', context=diction)


def barishal(request):
    divisionname = "barishal"
    diction = {"pmdata": pm25data(divisionname), "linechart": linechar(divisionname),  "boxplotchart": seasonwise(
        divisionname), "barchart": barchart(divisionname), "stationwiseboxplot": stationwise(divisionname), 'organization': orgnwise(divisionname), 'orgscatt': orgwisescatter(divisionname)}

    return render(request, 'barisaldash.html', context=diction)


def chittagong(request):
    divisionname = "Chittagong"
    diction = {"pmdata": pm25data(divisionname), "linechart": linechar(divisionname),  "boxplotchart": seasonwise(
        divisionname), "barchart": barchart(divisionname), "stationwiseboxplot": stationwise(divisionname), 'organization': orgnwise(divisionname), 'orgscatt': orgwisescatter(divisionname)}

    return render(request, 'chittagongdash.html', context=diction)


def mymensingh(request):
    divisionname = "Mymensingh"
    diction = {"pmdata": pm25data(divisionname), "linechart": linechar(divisionname),  "boxplotchart": seasonwise(divisionname), "barchart": barchart(
        divisionname), "stationwiseboxplot": stationwise(divisionname), 'organization': orgnwise(divisionname), 'orgscatt': orgwisescatter(divisionname)}

    return render(request, 'mymensinghdash.html', context=diction)
