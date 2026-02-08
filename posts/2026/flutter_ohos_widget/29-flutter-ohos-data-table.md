# Flutter for OpenHarmony 实战之基础组件：第二十九篇 Table 与 DataTable — 结构化数据展示专家

## 前言

在企业级应用或管理系统中，以行和列的形式展示结构化数据是最基本的需求。无论是财务报表、用户名单还是库存清单，一个能够支持排序、选择与自定义样式的表格组件，能极大地提升后台管理类业务的生产力。

在 **Flutter for OpenHarmony** 开发中，我们拥有两种处理表格的方案：轻量级的 `Table`（用于精细控制布局）和功能丰富的 `DataTable`（用于数据交互）。本文将带你掌握这两种表格的使用场景及在鸿蒙设备上的进阶玩法。

---

## 一、轻量级布局：Table

`Table` 类似于 HTML 中的 `<table>`，它严格保证每一行中相同索引的单元格宽度一致。

### 1.1 适用场景
当你需要构建一个简单的网格布局（如九宫格菜单、属性参数表），且不需要复杂的排序和多选功能时，`Table` 是性能更优的选择。

### 1.2 基础代码实现
```dart
Table(
  // 设置列宽占比
  columnWidths: const {
    0: FixedColumnWidth(80),   // 第一列固定宽度
    1: FlexColumnWidth(),      // 第二列自适应
    2: IntrinsicColumnWidth(), // 第三列根据内容定宽
  },
  // 设置边框
  border: TableBorder.all(color: Colors.grey[300]!, width: 1),
  children: [
    _buildTableRow(['参数', '值', '备注'], isHeader: true),
    _buildTableRow(['品牌', '华为', 'HUAWEI']),
    _buildTableRow(['系统', '鸿蒙', 'HarmonyOS NEXT']),
  ],
)
```

---

## 二、功能级展示：DataTable

`DataTable` 属于 Material 组件库，它内置了列头点击排序、行选中变色以及页码控制等高阶功能。

### 2.1 核心术语
- `DataColumn`: 定义表头。
- `DataRow`: 定义数据行。
- `DataCell`: 定义单元格内容。

### 2.2 实现排序与交互
```dart
DataTable(
  sortColumnIndex: _currentSortIndex,
  sortAscending: _isAscending,
  columns: [
    DataColumn(
      label: const Text('姓名'),
      onSort: (columnIndex, ascending) {
        // 在这里执行数据排序逻辑
        setState(() {
          _currentSortIndex = columnIndex;
          _isAscending = ascending;
        });
      },
    ),
    const DataColumn(label: Text('年龄'), numeric: true), // 数字列通常右对齐
  ],
  rows: users.map((u) => DataRow(
    cells: [
      DataCell(Text(u.name)),
      DataCell(Text('${u.age}')),
    ],
  )).toList(),
)
```

<!-- IMAGE_PLACEHOLDER: 具有排序功能的 DataTable 在鸿蒙设备上的运行截图 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙手机 -->

---

## 三、进阶：PaginatedDataTable 分页表格

当数据量达到成千上万条时，一次性渲染 `DataTable` 会导致页面卡顿。此时应使用“分页表格”。

### 3.1 分页组件结构
`PaginatedDataTable` 需要配合 `DataTableSource` 使用。

```dart
class UserDataSource extends DataTableSource {
  @override
  DataRow? getRow(int index) {
    if (index >= data.length) return null;
    final user = data[index];
    return DataRow.byIndex(
      index: index,
      cells: [DataCell(Text(user.name)), DataCell(Text('${user.id}'))],
    );
  }
  // ... 其他重写方法
}

// 页面中使用
PaginatedDataTable(
  header: const Text('员工列表'),
  source: _myDataSource,
  rowsPerPage: 8, // 每页显示行数
)
```

<!-- IMAGE_PLACEHOLDER: 分页表格在鸿蒙平板上的大屏布局展示 -->
<!-- 类型: 截图 -->
<!-- 设备: 鸿蒙平板 -->

---

## 四、OpenHarmony 平台适配建议

### 4.1 水平滚动兼容性
表格通常宽度较大，在窄屏手机上会出现溢出。

✅ **推荐方案**：
将 `DataTable` 包裹在 `SingleChildScrollView` 中，并设置 `scrollDirection: Axis.horizontal`。在鸿蒙系统上，横向滑动手势非常灵敏，配合弹性回弹效果体验极佳。

```dart
SingleChildScrollView(
  scrollDirection: Axis.horizontal,
  child: DataTable(...),
)
```

### 4.2 触控点击反馈
在鸿蒙设备上，当用户点击某一行进行选择时，默认的波纹效果（InkWell）能提供良好的反馈。

💡 **技巧**：
对于需要频繁点击的表格项，建议适当增加 `DataRow` 的高度，并在点击回调中触发 HapticFeedback。

### 4.3 宽屏适配建议
在鸿蒙平板横屏模式下，表格会出现大量留白。

✅ **最佳实践**：
- 使用 `Table` 的 `FlexColumnWidth` 自动填充剩余空间。
- 在 `DataTable` 中，通过 `columnSpacing` 属性动态调整列间距，避免在大屏上内容过于拥挤在左侧。

---

## 五、完整示例代码

以下演示一个支持“数据排序”和“多行选择”的综合表格示例。

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: DataTableDemo()));

class UserSimple {
  final String name;
  final int score;
  bool selected = false;
  UserSimple(this.name, this.score);
}

class DataTableDemo extends StatefulWidget {
  const DataTableDemo({super.key});

  @override
  State<DataTableDemo> createState() => _DataTableDemoState();
}

class _DataTableDemoState extends State<DataTableDemo> {
  final List<UserSimple> _users = [
    UserSimple("张三", 85),
    UserSimple("李四", 92),
    UserSimple("王五", 78),
    UserSimple("赵六", 88),
  ];
  
  int? _sortColumnIndex;
  bool _isAscending = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OHOS 数据表格实战')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const _SectionTitle("核心成就榜 (DataTable)"),
            _buildDataTable(),
            const SizedBox(height: 40),
            const _SectionTitle("轻量布局示列 (Table)"),
            _buildSimpleTable(),
          ],
        ),
      ),
    );
  }

  Widget _buildDataTable() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: DataTable(
          sortColumnIndex: _sortColumnIndex,
          sortAscending: _isAscending,
          columns: [
            const DataColumn(label: Text('学号')),
            DataColumn(
              label: const Text('姓名'),
              onSort: (idx, asc) => _sort<String>((u) => u.name, idx, asc),
            ),
            DataColumn(
              label: const Text('分数'),
              numeric: true,
              onSort: (idx, asc) => _sort<num>((u) => u.score, idx, asc),
            ),
          ],
          rows: _users.map((u) => DataRow(
            selected: u.selected,
            onSelectChanged: (v) => setState(() => u.selected = v!),
            cells: [
              DataCell(Text("2024${_users.indexOf(u)}")),
              DataCell(Text(u.name)),
              DataCell(Text("${u.score}")),
            ],
          )).toList(),
        ),
      ),
    );
  }

  Widget _buildSimpleTable() {
    return Table(
      border: TableBorder.all(color: Colors.grey.shade300, borderRadius: BorderRadius.circular(8)),
      columnWidths: const {0: FixedColumnWidth(60)},
      children: [
        const TableRow(children: [Center(child: Text("ID")), Center(child: Text("属性")), Center(child: Text("状态"))]),
        _tableRow("1", "网络连接", "已在线"),
        _tableRow("2", "存储空间", "正常"),
      ],
    );
  }

  TableRow _tableRow(String c1, String c2, String c3) {
    return TableRow(children: [
      Padding(padding: const EdgeInsets.all(8), child: Center(child: Text(c1))),
      Padding(padding: const EdgeInsets.all(8), child: Text(c2)),
      Padding(padding: const EdgeInsets.all(8), child: Text(c3, style: const TextStyle(color: Colors.green))),
    ]);
  }

  void _sort<T>(Comparable<T> Function(UserSimple user) getField, int colIdx, bool asc) {
    setState(() {
      _sortColumnIndex = colIdx;
      _isAscending = asc;
      _users.sort((a, b) {
        final aVal = getField(a);
        final bVal = getField(b);
        return asc ? Comparable.compare(aVal, bVal) : Comparable.compare(bVal, aVal);
      });
    });
  }
}

class _SectionTitle extends StatelessWidget {
  final String title;
  const _SectionTitle(this.title);
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueGrey)),
    );
  }
}
```

---

## 六、总结

在 Flutter for OpenHarmony 的企业级应用开发中，选择合适的表格组件对于提升数据处理效率至关重要。

1.  **Table**：追求性能和极致布局控制时的首选，尤其适合作为小组件内部的骨架图。
2.  **DataTable**：业务逻辑驱动时的专家，能低成本实现排序、选择等交互。
3.  **用户体验**：在鸿蒙端，利用好 `SingleChildScrollView` 的横向滚动特性，并通过样式定制淡化表格的“生硬感”，使其更好地融入鸿蒙系统的 UI 语境。

---

📦 **完整代码已上传至 AtomGit**：[flutter_ohos_examples](https://atomgit.com/dragonbady/flutter_ohos_examples)

🌐 **欢迎加入开源鸿蒙跨平台社区**：[开源鸿蒙跨平台开发者社区](https://openharmonycrossplatform.csdn.net)

---

