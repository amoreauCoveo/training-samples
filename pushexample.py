from coveopush import CoveoPush
from coveopush import Document
from coveopush import CoveoPermissions
from coveopush import CoveoConstants
import json

# The settings of your source and organization
settings = {
    "sourceId": "your-source-id",
    "orgId": "your-org-id",
    "apiKey": "your-api-key"
}

# Define push so we know where to send
push = CoveoPush.Push(settings["sourceId"], settings["orgId"], settings["apiKey"])

# Define a URI. This has to be in the URL format, but doesn't have to be a URL
# It's simpler to put the link that opens the actual document here, though it's not mandatory
mydoc = Document("https://www.example.com")

# Titles are very useful, and are useful by a lot of default Coveo components
# If you don't enter a title, the URI value would normally be taken instead
mydoc.Title = "THIS IS A TEST"

# The body of the document contians the actual content of your documents. It is also used to generate the quickview
# Not having a body can make it very hard to find your documents. Make sure you set the right things here
mydoc.SetData("ALL OF THESE WORDS ARE SEARCHABLE")

# The file extension helps Coveo understand how to parse your content.
# A .html extension tells Coveo to treat the body as HTML, and will thus ignore the tags themselves, and just index the content.
mydoc.FileExtension = ".html"

# Any additional metadata can then be added
# In this example, we add the value "CSV" to a field called "connectortype"
mydoc.AddMetadata("connectortype", "CSV")

push_in_batch = False
if (push_in_batch):
    # This action sends a single document to Coveo
    # This is fine for testing, but it shouldn't be used when sending multiple items
    # Otherwise, some items will fail to be added, returning the 429 response
    push.AddSingleDocument(mydoc)
else:
    # If you instead wanted to push a bunch of items, you would need to do the following instead
    item_batch = []
    item_batch.append(mydoc)
    # Of course, feel free to add as many items as you would like here

    # We want to update the status of the source when pushing
    # You typically almost always want this option set to true
    updateSourceStatus = True
    # If you want to clear the whole source before pushing new content, set this to True
    # But most of the time you might just want to push or update new content
    deleteOlder = False
    
    # You can then push the documents to Coveo. The SDK takes care of creating the batches for you
    # The first argument is an array of items to add, and the second is an array of items to delete
    # The last two are explained above
    push.AddDocuments(item_batch, [], updateSourceStatus, deleteOlder)