from tool import Tool
import colors
class Pickuparea:
    """Implementation of a pickup location."""
 
    def __init__(self, tool, x, y):
        '''
        :param Tool tool: Tool object located at pickup area
        :param int x: pickup x coordinate
        :param int y: pickup y coordinate

        '''
	self.tool = tool
	self.x = x
	self.y = y
  
    def getToolName(self):
        '''
        :return string: Name of tool at location
        '''
        return self.tool.NAME


    def getXY(self):
        '''
        :return int self.x: x coordinate
        :return int self.y: y coordinate
        '''
	return self.x, self.y

    def empty(self):
        '''
        :return bool: True if pickup location is empty
        '''
	return True if self.tool == "empty" else False

    def releaseItem(self):
        '''
        :return tool self.tool: releases tool
        '''
	tmpTool = self.tool
	self.tool = "empty"
        return tmpTool

    def getColor(self):
        '''
        :return list int: Tool color
        '''
	return colors.EMPTY_TILE if self.empty() else self.tool.getColor()
 
    def receiveTool(self, tool):
        '''
        :param tool tool: tool placed in pickup location by agent
        '''
        self.tool = tool
