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