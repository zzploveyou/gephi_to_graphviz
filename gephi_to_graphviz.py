# coding:utf-8
import csv
import os
import re
import sys
import argparse

class DynamicGraphviz:
    """将gephi的动态网路图点边数据转化为graphviz形式的dot文件"""

    def __init__(self, nodefile="nodeDY.csv", edgefile="edgeDY.csv", edgeweight=0):
        self.nodefile = nodefile
        self.edgefile = edgefile
        self.path = os.path.dirname(self.nodefile)
        self.outfilename = os.path.join(
            self.path, "result-edgefilt-" + str(edgeweight) + ".dot")
        self.edgeweight = edgeweight
        self.colors = ['skyblue', 'firebrick1', 'mediumseagreen',
                       'aquamarine', 'antiquewhite1', 'cyan1', 'lavenderblush',
                       'palegoldenrod', 'palegreen', 'mistyrose1', 'plum2']
        self.colors_tag = 0
        self.type_color = {}
        self.nodes = set()
        self.nodelines = []
        self.edgelines = []

    def go(self):
        """先根据传入参数获取过滤的边,然后根据有边的点,再添加点的信息
        最后得到结果"""

        # gephi格式的边信息 edgelines
        self.get_edge_format_gephi()
        # gephi格式的节点 nodelines
        self.get_node_format_gephi()

        self.write_result()

    def get_node_format_nature(self):
        pass

    def get_edge_format_nature(self):
        pass

    def get_node_format_gephi(self):
        """根据node.csv获取graphviz格式的节点信息"""
        if not os.path.exists(self.nodefile):
            return
        csvfile = open(self.nodefile)
        reader = csv.reader(csvfile)
        pattern = re.compile(r';.*,(.*)];>')
        for linelist in reader:
            name = linelist[0]
            ty = linelist[2]
            # ...;[2014.5,2015.5,0.012195];>"
            try:
                value = float(re.search(pattern, linelist[3]).group(1))
                # print name,ty,value
                if ty not in self.type_color:
                    if self.colors_tag >= len(self.colors):
                        self.colors_tag %= len(self.colors)
                    # print ty, self.colors_tag
                    self.type_color[ty] = self.colors[self.colors_tag]
                    self.colors_tag += 1
                # 信息 [color = mediumseagreen, style = filled, fontsize = 30];
                if name in self.nodes:
                    '''没有边的不添加'''
                    line = '%s\"%s\" [color=%s, style=%s, fontsize=%s];\n' % (
                        "    ", name, self.type_color[ty], "filled", 10)
                    self.nodelines.append(line)
            except AttributeError as e:
                pass
        # print self.nodelines

    def get_edge_format_gephi(self):
        """根据edge.csv获取graphviz格式的边信息"""
        if not os.path.exists(self.edgefile):
            return
        csvfile = open(self.edgefile)
        reader = csv.reader(csvfile)
        pattern = re.compile(r';.*,(.*)\);>')
        for linelist in reader:
            targetA = linelist[0]
            targetB = linelist[1]
            # 0.010870);[2014.5,2015.5,0.008130);>
            try:
                value = float(re.search(pattern, linelist[4]).group(1))
                # print value
                # a -- b [penwidth = 1, style = filled]
                if value >= self.edgeweight:
                    line = '%s\"%s\" -- \"%s\" [penwidth=%s, style=%s];\n' % (
                        "    ", targetA, targetB, 1, "filled")
                    self.nodes.add(targetA)
                    self.nodes.add(targetB)
                    self.nodelines.append(line)
            except AttributeError as e:
                pass

    def write_result(self):
        fw = open(self.outfilename, 'w')
        fw.write("graph s{\n")
        fw.writelines(self.nodelines)
        fw.writelines(self.edgelines)
        fw.write("}")
        fw.close()

def parse():
    parser = argparse.ArgumentParser(
        description='description: get graphviz dot format file, \
            author: Zhaopeng Zhang')
    parser.add_argument('-n', '--node', type=str,
                        help='nodefile path.')
    parser.add_argument('-e', '--edge', type=str,
                        help='edgefile path.')
    parser.add_argument('-f', '--filt', type=float,default=0,
                        help='filt edge weight.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = parse()
    dg = DynamicGraphviz(nodefile=args.node, edgefile=args.edge, edgeweight=args.filt)
    dg.go()
