# PyBulma

PyBulma is yet another libray for us python coders, to make frontend work more palatable. The big difference
is that PyBulma is based on using the Bulma.io css library and also generating smaller html snippets that can
be used as includes for the Jinja2/Django Templating libraries. The whole idea is that we can use PyBulma to
create something like Web components on the backend.

## Why Bulma.io

Bulma is a pretty good CSS library, and it's VERY easy to use. Its layouts are clean and simple. It also allows 
us to think in terms of components that are to be added to web pages, instead of HTML and CSS. In this I mean
we think in terms of adding a header, modal, table etc, instead of divs, spans, and other tags.

## PyBulma Component Classes

With the PyBulma classes, a lot of the work for adding components is already done for you. It adds most
of the basic Bulma classes for you, while allowing you to add additional classes, style and attributes if needed.
Also, each Object can themselves hold 0 or more subcomponents, who's html will be rendered between the parents
opening and closing html.

These are simple classes really, but it allows you to think and work on components instead of html tags and classes.

The second advantage of this, is that often two or more items in web pages need to be linked, such as the button
to open a modal, and the modal itself. However, when you code in html, you either need to add these as separate 
include files, or add them all to the same file in widely different places. It makes upkeep hard.

With PyBulma, we can create the modal and the button objects at the same time, then add them to different parent 
objects, so while in the html, they are not together, in our code they are.

## PyBulma Example

In this example, I am going to create a table. Not a complex task, but one that shows, how components and sub-components
work

Since we are working on objects, we can start with the Table, create the sub items, and then add them to the table,
or we can just create the sub items and then create the table and add them. I will use the latter

```python
from pybulma.table import Table, TableHead, HeadCell, TableBody, TableRow, TableCell
from pybulma.buttons import ButtonGroup, ButtonLink

# Create the table headers. abbr adds the bulma abbreviation component
header = TableHead()
header.add(HeadCell("Name"))
header.add(HeadCell("Address", abbr="Addr"))
header.add(HeadCell("Current Status", abbr="Status"))
header.add(HeaderCell("Actions"))

# Main table body. Unlike TableHead, the row is not included as you might want to set classes and id on the row
body = TableBody(data_variable="table1", row_variable="row", table_body_id="tabl_{{ table_no }}")
row = TableRow()
row.add(TableCell(cell_content="{{ row.name }}"))
row.add(TableCell(cell_content="{{ row.address1}}<br>{{ row.address2 }}"))
row.add(TableCell(cell_content="{{ row.status|lower }}"))

# Creating a Bulma button Group to be added to the table for actions
# ButtonLink creates a button using an anchor tag. Button color can be set using the color parameter or the classes parameter
actions = ButtonGroup()
actions.add(ButtonLink(url="/item/update/{{ row.id }}/", button_text="Update", color="is-warning"))
actions.add(ButtonLink(url="/item/delete/{{row.id}}/"), button_text="delete", color="is-danger")
# TableCell created with no contents as its contents will be the button group as a subcomponent
table_actions = TableCell()
table_actions.add(actions)
row.add(table_actions)

body.add(row)
table = Table()
table.add(header)
table.add(body)
# simple save that will compile and save the html. You can run this multiple times 
# for different files, so you can change an object after a save and then save the changes again
table.save("/includes/table1.html")
```

So lets go through this. I created the Table Header component and added header cells into it. The *abbr*
add the abbreviation classes from Bulma, so that the abbr text value is shown, but the main text is show
when moused over.

Table body, row and cell are separate objects, because in a lot of instances, we need to apply classes, styles,
or id's to each of those elements. The row in the header is put in by default because there is no need to
apply changes to that element.

for the Table body, the data_variable and row_variables are used in a for loop that surrounds the row and cells.
so its  ** for row_variable in data_variable**. table_body_id is used to set an id for the body element, but this
is optional.

TableRow creates the *<tr></tr>* tags, which you will notice wasn't required for the TableHead. This is
because the rows in the body will often require their on id, classes or styles set, while the row in the 
header does not

The table cells are just passed an argument of cell_content. This allows you to pass a text item. The items
here are Jinja2 template items, but you could just as easily create and compile a button group and pass that as 
a subcomponent as shown

You will also notice that the text items are template text variables, showing this is creating a template,
not the final html.

Is coding this faster than coding the templates? Well I don't think so, but working with objects and components
just looks and feels better to me, more pyronic. It also allows you to create your own sets of python web components
that can be called and added to web pages. For example, the above code could all be placed in a function
and you just pass the parameters needed to the function, thus creating the table in a couple of lines.

## Which items are made into components

I am attempting to stay away from any basic html tag components as I would like to think of the items
in their component name, rather than their tag, but there are some instances, when it might be needed.
I have added a HtmlTag component to allow for flexibility. I've not come across a need for it yet, but
it might happen. 

## Brython

Keeping with the pyronic theme, I have added some scripts using Brython. It's not pure python, and you
do need to understand the javascript dom concepts, but it is a lot more comfortable to use and gives
access to some javascript items that are poorly documented elsewhere.