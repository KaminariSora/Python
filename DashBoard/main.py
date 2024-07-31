import dash 
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1('My DashBoard'),
        dcc.Graph(
            id='My-Graph',
            figure={
                'Data':[
                    {'x':[1,2,3], 'y':[4,1,2],'type': 'bar', 'name':'Bar Chart'},
                    {'x':[1,2,3], 'y':[4,1,2],'type': 'line', 'name':'Line Chart'},
                ],
                'layout':{
                    'title':'Graph title',
                    'xaxis': {'title': 'x-axis'},
                    'yaxis': {'title': 'y-axis'},
                }
            }
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)