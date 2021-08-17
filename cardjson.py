card_input = [
   {
      "contentType":"application/vnd.microsoft.card.adaptive",
      "content":{
         "type":"AdaptiveCard",
         "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
         "version":"1.2",
         "body":[
            {
               "type":"ColumnSet",
               "columns":[
                  {
                     "type":"Column",
                     "width":"stretch",
                     "items":[
                        {
                           "type":"Image",
                           "url":"https://media-exp1.licdn.com/dms/image/C5612AQEdv0AE31r-3A/article-cover_image-shrink_423_752/0/1548189396921?e=1634169600&v=beta&t=Kdp8aLGQpm9R0N1gRR6YAHJCmidH39PsRx8TV22ab28"
                        }
                     ]
                  },
                  {
                     "type":"Column",
                     "width":"stretch",
                     "items":[
                        {
                           "type":"TextBlock",
                           "text":"This is SD-WAN bot.",
                           "wrap":True,
                           "size":"Medium",
                           "weight":"Bolder"
                        },
                        {
                           "type":"TextBlock",
                           "text":"Supported commands are:",
                           "wrap":True
                        }
                     ]
                  }
               ]
            },
            {
               "type":"Input.Toggle",
               "title":"show users",
               "id":"0"
            },
            {
               "type":"Input.Toggle",
               "title":"show devices",
               "id":"1"
            },
            {
               "type":"Input.Toggle",
               "title":"show controllers",
               "id":"2"
            },
            {
               "type":"Input.Toggle",
               "id":"3",
               "title":"show vedges"
            },
            {
               "type":"ActionSet",
               "actions":[
                  {
                     "type":"Action.Submit",
                     "title":"Submit"
                  }
               ]
            }
         ]
      }
   }
]

card_output = [
   {
      "contentType":"application/vnd.microsoft.card.adaptive",
      "content":{
         "type":"AdaptiveCard",
         "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
         "version":"1.2",
         "body":[
            {
               "type":"ColumnSet",
               "columns":[
                  {
                     "type":"Column",
                     "width":"stretch",
                     "items":[
                        {
                           "type":"Image",
                           "url":"https://media-exp1.licdn.com/dms/image/C5612AQEdv0AE31r-3A/article-cover_image-shrink_423_752/0/1548189396921?e=1634169600&v=beta&t=Kdp8aLGQpm9R0N1gRR6YAHJCmidH39PsRx8TV22ab28"
                        }
                     ]
                  },
                  {
                     "type":"Column",
                     "width":"stretch",
                     "items":[
                        {
                           "type":"TextBlock",
                           "text":"Results for",
                           "wrap":True,
                           "size":"Medium",
                           "weight":"Bolder"
                        },
                        {
                           "type":"TextBlock",
                           "text":"show command",
                           "wrap":True
                        }
                     ]
                  }
               ]
            },
            {
               "type":"TextBlock",
               "text":"Here goes the text",
               "wrap":True
            }
         ]
      }
   }
]

project1_card_input=[{
	"contentType": "application/vnd.microsoft.card.adaptive",
	"content":


{
    "type": "AdaptiveCard",
    "version": "1.2",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://community.cisco.com/t5/image/serverpage/image-id/118223iB1C5F59EC782C05C?v=v2",
                            "size": "Medium"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "SD-WAN Demo",
                            "wrap": True,
                            "weight": "Bolder",
                            "size": "Medium",
                            "color": "Accent"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Chatbot demo assisting with configuring, monitoring and analysing data.",
                            "wrap": True,
                            "color": "Good"
                        }
                    ]
                }
            ]
        },
        {
            "type": "Container",
            "items": [
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "CONFIGURE",
                                    "wrap": True,
                                    "weight": "Bolder",
                                    "separator": True
                                },
                                {
                                    "type": "ActionSet",
                                    "actions": [
                                        {
                                            "type": "Action.Submit",
                                            "title": "New network",
                                            "iconUrl": "https://cdn0.iconfinder.com/data/icons/virtual-reality-1-1/50/25-512.png",
                                            "id": "0",
                                            "data": {
                                                "button": "new_network"
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "MONITOR",
                                    "wrap": True,
                                    "weight": "Bolder",
                                    "separator": True
                                },
                                {
                                    "type": "ActionSet",
                                    "actions": [
                                        {
                                            "type": "Action.Submit",
                                            "title": "Show",
                                            "iconUrl": "https://icons-for-free.com/iconfiles/png/512/desktop+laptop+mac+monitor+pc+screen+icon-1320084900181856200.png",
                                            "id": "1",
                                            "data": {
                                                "button": "show"
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "ANALYSE",
                                    "wrap": True,
                                    "weight": "Bolder",
                                    "separator": True
                                },
                                {
                                    "type": "ActionSet",
                                    "actions": [
                                        {
                                            "type": "Action.Submit",
                                            "title": "Backup",
                                            "id": "2",
                                            "iconUrl": "https://image.flaticon.com/icons/png/512/477/477890.png",
                                            "data": {
                                                "button": "backup"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "separator": True
                }
            ],
            "style": "accent"
        },
        {
            "type": "Input.ChoiceSet",
            "choices": [
                {
                    "title": "title",
                    "value": "pera"
                }
            ],
            "placeholder": "Selected option",
            "id": "55",
            "value": "lala",
            "isVisible": False
        }
    ]
}
}]