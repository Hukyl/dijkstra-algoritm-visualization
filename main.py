"""
This module provides Tkinter windows and frames to visualize Dijkstra's algorithm
Classes:
    - Indexed Node: node with autoincremented index
    - Color: enumeration of colors and their hex values
    - LineAskingDialog: Tkinter frame for creating connection between nodes on the canvas
    - SolveAskingDialog: Tkinter frame for direction of solving the graph
    - MainWindow: Tkinter frame for hosting the visualization of Dijkstra's algorithm
"""
# pylint: disable=R0902, C0103, E0401

from enum import Enum
import pickle
import tkinter as tk
from tkinter import messagebox, filedialog

from solver import Node, DijkstraGraphSolver


class IndexedNode(Node):
    """Graph node with index."""
    COUNT = 0

    def __new__(cls, *args, **kwargs):
        cls.COUNT += 1
        return super(cls, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        super().__init__()
        self.index = self.COUNT

    def __repr__(self):
        return f"IndexedNode(index={self.index})"

    def __del__(self):
        self.__class__.COUNT -= 1


class Color(Enum):
    """Color and corresponding hex value."""
    WHITE = '#fff'
    RED = '#f00'
    GREEN = '#006400'
    BLACK = '#000'
    BLUE = '#00f'


class LineAskingDialog(tk.Frame):
    """Ask for line"""

    def __init__(self, master=None, **options):
        super().__init__(master, **options)
        self.initUi()

    def initUi(self):
        """Init window"""
        self.width, self.height = 300, 100
        position_right = int(screen_width / 2 - self.width / 2)
        position_down = int(screen_height / 2 - self.height / 2)
        self.master.geometry(
            f"{self.width}x{self.height}+{position_right}+{position_down}"
        )
        self.master.resizable(width=False, height=False)
        self.master.title("Build a line")
        self.master.columnconfigure(0, weight=2)
        self.master.columnconfigure(1, weight=3)
        self.fromNodeLabel = tk.Label(
            self.master, text="From:", anchor=tk.W
        )
        self.fromNodeContent = tk.IntVar()
        self.fromNodeEdit = tk.Entry(self.master)
        self.fromNodeEdit['textvariable'] = self.fromNodeContent
        self.fromNodeLabel.grid(row=0, column=0, sticky="ew")
        self.fromNodeEdit.grid(row=0, column=1, sticky="ew", padx=5)
        self.toNodeLabel = tk.Label(
            self.master, text="To:", anchor=tk.W
        )
        self.toNodeContent = tk.IntVar()
        self.toNodeEdit = tk.Entry(self.master)
        self.toNodeEdit['textvariable'] = self.toNodeContent
        self.toNodeLabel.grid(row=1, column=0, sticky="ew")
        self.toNodeEdit.grid(row=1, column=1, sticky="ew", padx=5)
        self.valueLabel = tk.Label(
            self.master, text="Value:", anchor=tk.W
        )
        self.valueContent = tk.IntVar()
        self.valueEdit = tk.Entry(self.master)
        self.valueEdit['textvariable'] = self.valueContent
        self.valueLabel.grid(row=2, column=0, sticky="ew")
        self.valueEdit.grid(row=2, column=1, sticky="ew", padx=5)
        self.submitButton = tk.Button(
            self.master, anchor=tk.CENTER, text="Submit"
        )
        self.submitButton.grid(
            row=3, column=0,
            sticky='ew', padx=40, pady=5,
            columnspan=2
        )


class SolveAskingDialog(tk.Frame):
    """Ask for solve nodes"""

    def __init__(self, master=None, **options):
        super().__init__(master, **options)
        self.initUi()

    def initUi(self):
        """Init window"""
        self.width, self.height = 300, 80
        position_right = int(screen_width / 2 - self.width / 2)
        position_down = int(screen_height / 2 - self.height / 2)
        self.master.geometry(
            f"{self.width}x{self.height}+{position_right}+{position_down}"
        )
        self.master.resizable(width=False, height=False)
        self.master.title("Solve graph")
        self.master.columnconfigure(0, weight=2)
        self.master.columnconfigure(1, weight=3)
        self.fromNodeLabel = tk.Label(
            self.master, text="From:", anchor=tk.W
        )
        self.fromNodeContent = tk.IntVar()
        self.fromNodeEdit = tk.Entry(self.master)
        self.fromNodeEdit['textvariable'] = self.fromNodeContent
        self.fromNodeLabel.grid(row=0, column=0, sticky="ew")
        self.fromNodeEdit.grid(row=0, column=1, sticky="ew", padx=5)
        self.toNodeLabel = tk.Label(
            self.master, text="To:", anchor=tk.W
        )
        self.toNodeContent = tk.IntVar()
        self.toNodeEdit = tk.Entry(self.master)
        self.toNodeEdit['textvariable'] = self.toNodeContent
        self.toNodeLabel.grid(row=1, column=0, sticky="ew")
        self.toNodeEdit.grid(row=1, column=1, sticky="ew", padx=5)
        self.submitButton = tk.Button(
            self.master, anchor=tk.CENTER, text="Submit"
        )
        self.submitButton.grid(
            row=3, column=0,
            sticky='ew', padx=40, pady=5,
            columnspan=2
        )


class MainWindow(tk.Frame):
    """Main Window"""
    TO_DRAW_NODE = False
    NODE_CIRCLE_RADIUS = 15
    LINE_SQUARE_RADIUS = 10
    WRONG_NODE_LINE_RADIUS = int(1.25 * NODE_CIRCLE_RADIUS)
    NODE_TEXT_YMARGIN = int(NODE_CIRCLE_RADIUS / 2)
    NODE_TEXT_XMARGIN = int(NODE_CIRCLE_RADIUS / 4)
    LINE_TEXT_XMARGIN = int(LINE_SQUARE_RADIUS / 3)
    LINE_TEXT_YMARGIN = int(LINE_SQUARE_RADIUS / 5 * 4)
    NODES = []

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.width, self.height = 1080, 720
        position_right = int(screen_width / 2 - self.width / 2)
        position_down = int(screen_height / 2 - self.height / 2)
        self.master.geometry(
            f"{self.width}x{self.height}+{position_right}+{position_down}"
        )
        self.master.title("Dijkstra's algorithm")
        self.master.resizable(width=False, height=False)
        self.initUI()
        self.lineWindow = None
        self.solveWindow = None

    def initUI(self):
        """
        Initialize UI.
        """
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Import...", command=self.importGraph)
        fileMenu.add_command(label="Export...", command=self.exportGraph)
        menu.add_cascade(label="File", menu=fileMenu)
        addMenu = tk.Menu(menu)
        addMenu.add_command(label="Node", command=self.setDrawFlag)
        addMenu.add_command(label="Line", command=self.createLineAskingDialog)
        menu.add_cascade(label="Add", menu=addMenu)
        menu.add_command(label="Reset", command=self.resetCanvas)
        menu.add_command(label="Redraw", command=self.redrawCanvas)
        menu.add_command(label="Solve", command=self.createSolveAskingDialog)
        self.statusbar_frame = tk.Frame(
            self.master, bd=1
        )
        self.statusbar_frame.columnconfigure(0, weight=20)
        self.statusbar_frame.columnconfigure(1, weight=1)
        self.statusbar = tk.Label(
            self.statusbar_frame, text="",
            bd=.5, relief=tk.SUNKEN, anchor=tk.W
        )
        self.cursorPosition = tk.Label(
            self.statusbar_frame, text="",
            bd=.5, relief=tk.SUNKEN, anchor=tk.W
        )
        self.statusbar.grid(row=0, column=0, sticky="ew")
        self.cursorPosition.grid(row=0, column=1, sticky="ew")
        self.statusbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas = tk.Canvas(self.master, bg=Color.WHITE.value)
        self.canvas.bind("<Button-1>", self.createNode)
        self.canvas.bind('<Motion>', self.showCursorPosition)
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def redrawCanvas(self):
        """
        Clear the canvas and redraw each line and node.
        """
        self.canvas.delete("all")
        for node_data in self.NODES:
            node_data['node'].reset()
            for neighbor_node, path_cost in node_data['node'].neighbors.items():
                neighbor_node = self.NODES[neighbor_node.index - 1]
                self.drawLine(
                    node_data['position'], neighbor_node['position'], path_cost
                )
                self.drawNode(
                    neighbor_node['node'].index, neighbor_node['position']
                )
                self.drawNode(
                    node_data['node'].index, node_data['position']
                )

    def importGraph(self):
        """Import graph, by asking user for .pickle objects"""
        self.statusbar['text'] = 'Importing graph...'
        file = filedialog.askopenfile(
            parent=self.master,
            mode='rb', title="Import Pickle",
            filetypes=[('*', '.pickle')]
        )
        self.statusbar['text'] = ''
        if file is None:
            return
        self.NODES = pickle.load(file)
        IndexedNode.COUNT = len(self.NODES)
        self.redrawCanvas()

    def exportGraph(self):
        """Export graph by asking user to save file in .pickle extension"""
        file = filedialog.asksaveasfile(
            parent=self.master,
            mode='wb', title='Export Pickle',
            defaultextension='pickle'
        )
        if file is None:
            return
        pickle.dump(self.NODES, file)
        file.close()

    def setDrawFlag(self):
        """
        Activate node draw mode.
        """
        self.TO_DRAW_NODE = True
        self.statusbar['text'] = 'Click on canvas to set a node...'
        self.canvas['cursor'] = 'tcross'

    def drawNode(
            self, index: int,
            position: tuple, *, outline: str = Color.GREEN.value
            ):
        """
        Draw a node with an index.

        Args:
            index (int)
            position (tuple): (x, y) of point
            outline (str, optional): outline of node circle. Defaults to Color.GREEN.value.
        """
        x, y = position
        self.canvas.create_oval(
            x - self.NODE_CIRCLE_RADIUS, # from x
            y - self.NODE_CIRCLE_RADIUS, # from y
            x + self.NODE_CIRCLE_RADIUS, # to x
            y + self.NODE_CIRCLE_RADIUS, # to y
            outline=outline, fill=Color.WHITE.value
        )
        self.canvas.create_text(
            x - (
                self.NODE_TEXT_XMARGIN * len(str(index))
            ),
            y + self.NODE_TEXT_YMARGIN,
            text=str(index), anchor=tk.SW
        )

    def drawLine(
            self, pos_from: tuple, pos_to: tuple,
            value: int, *, fill: str = Color.BLACK.value
            ):
        """
        Draw a line between two points with a value.

        Args:
            pos_from (tuple): (x, y) start point
            pos_to (tuple): (x, y) end point
            value (int)
            fill (str, optional): line color. Defaults to Color.BLACK.value.
        """
        self.canvas.create_line(*pos_from, *pos_to, fill=fill)
        middle_pos = (
            int((pos_from[0] + pos_to[0]) / 2),
            int((pos_from[1] + pos_to[1]) / 2),
        )
        value_len = len(str(value))
        self.canvas.create_rectangle(
            middle_pos[0] - (
                self.LINE_SQUARE_RADIUS - self.LINE_TEXT_XMARGIN + (
                    self.LINE_TEXT_XMARGIN * value_len
                )
            ), # from x
            middle_pos[1] - self.LINE_SQUARE_RADIUS, # from y
            middle_pos[0] + (
                self.LINE_SQUARE_RADIUS - self.LINE_TEXT_XMARGIN + (
                    self.LINE_TEXT_XMARGIN * value_len
                )
            ), # to x
            middle_pos[1] + self.LINE_SQUARE_RADIUS, # to y
            fill=Color.WHITE.value, outline=fill
        )
        self.canvas.create_text(
            middle_pos[0] - (
                self.LINE_TEXT_XMARGIN * value_len
            ),
            middle_pos[1] + self.LINE_TEXT_YMARGIN,
            text=str(value), anchor=tk.SW
        )

    def createNode(self, event):
        """
        Draw a node on the canvas and add to the local storage.

        Args:
            event (_type_): Tkinter original click event
        """
        if self.TO_DRAW_NODE:
            position = (event.x, event.y)
            node = IndexedNode()
            self.NODES.append({
                'position': position,
                'node': node
            })
            self.drawNode(node.index, position)
            self.canvas['cursor'] = ''
            self.statusbar['text'] = ''
            self.TO_DRAW_NODE = False

    def createLineAskingDialog(self):
        """
        Create dialog window to create a line.
        """
        # pylint: disable=W0613
        self.lineWindow = LineAskingDialog(tk.Toplevel(self.master))
        self.lineWindow.submitButton.bind('<Button-1>', lambda event: self.addConnection())
        self.lineWindow.mainloop()

    def createSolveAskingDialog(self):
        """
        Create dialog window to ask solve the window.
        """
        # pylint: disable=W0613
        if len(self.NODES) < 2:
            messagebox.showerror("Error", "Too few nodes, add some more")
            return
        self.solveWindow = SolveAskingDialog(tk.Toplevel(self.master))
        self.solveWindow.submitButton.bind('<Button-1>', lambda event: self.solveGraph())
        self.solveWindow.mainloop()

    def addConnection(self):
        """
        Add a connection between nodes.

        Args:
            event (_type_): original Tkinter submit event
        """
        fromIndex = self.lineWindow.fromNodeContent.get()
        toIndex = self.lineWindow.toNodeContent.get()
        value = self.lineWindow.valueContent.get()
        try:
            fromNode = self.NODES[fromIndex - 1]
            toNode = self.NODES[toIndex - 1]
        except KeyError:
            messagebox.showerror("Error", 'Input only valid indexes')
            return
        if value <= 0:
            messagebox.showerror(
                "Error",
                "This implementation supports only positive path costs"
            )
            return
        fromNode['node'].connect(toNode['node'], value)
        self.drawLine(fromNode['position'], toNode['position'], value)
        self.drawNode(fromNode['node'].index, fromNode['position'])
        self.drawNode(toNode['node'].index, toNode['position'])
        self.lineWindow.master.destroy()
        self.lineWindow.master.update()
        self.lineWindow = None

    def showCursorPosition(self, event):
        """
        Display cursor position in the status bar.

        Args:
            event (_type_): original Tkinter click event
        """
        self.cursorPosition['text'] = f"({event.x}, {event.y})"

    def resetCanvas(self):
        """
        Clear the canvas and delete all nodes.
        """
        if messagebox.askyesno(
                title="Reset canvas",
                message="Do you wish to delete all your nodes and connections?"
            ):
            self.canvas.delete("all")
            self.NODES = []
            IndexedNode.COUNT = 0

    def solveGraph(self):
        """
        Draw path on graph with color markering and
        path cost on each of nodes in the resulting path.
        """
        fromIndex = self.solveWindow.fromNodeContent.get()
        toIndex = self.solveWindow.toNodeContent.get()
        try:
            fromNode = self.NODES[fromIndex - 1]
            toNode = self.NODES[toIndex - 1]
        except KeyError:
            messagebox.showerror("Error", 'Input only valid indexes')
            return
        self.solveWindow.master.destroy()
        self.solveWindow.master.update()
        self.solveWindow = None
        solver = DijkstraGraphSolver(
            first=fromNode['node'],
            last=toNode['node']
        )
        path = solver.get_path()
        for node in self.NODES:
            x, y = node['position']
            if node['node'] not in path:
                self.canvas.create_line(
                    x - self.WRONG_NODE_LINE_RADIUS,
                    y - self.WRONG_NODE_LINE_RADIUS,
                    x + self.WRONG_NODE_LINE_RADIUS,
                    y + self.WRONG_NODE_LINE_RADIUS,
                    fill=Color.RED.value
                )
                self.canvas.create_line(
                    x - self.WRONG_NODE_LINE_RADIUS,
                    y + self.WRONG_NODE_LINE_RADIUS,
                    x + self.WRONG_NODE_LINE_RADIUS,
                    y - self.WRONG_NODE_LINE_RADIUS,
                    fill=Color.RED.value
                )
            else:
                self.canvas.create_text(
                    x + self.WRONG_NODE_LINE_RADIUS, y,
                    text=str(node['node'].value_to_reach), anchor=tk.SW
                )
        for i in range(0, len(path) - 1):
            node_from = self.NODES[path[i].index - 1]
            node_to = self.NODES[path[i + 1].index - 1]
            self.drawLine(
                node_from['position'], node_to['position'],
                node_from['node'].neighbors[node_to['node']], fill=Color.GREEN.value
            )
            self.drawNode(
                node_from['node'].index,
                node_from['position'],
                outline=Color.BLUE.value
            )
            self.drawNode(
                node_to['node'].index,
                node_to['position'],
                outline=Color.BLUE.value
            )



if __name__ == '__main__':
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app = MainWindow(root)
    root.mainloop()
