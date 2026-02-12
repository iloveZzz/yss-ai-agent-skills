---
name: "yss-excel-mvc"
description: "封装 Spring MVC 的 Excel 导入导出能力。用户需要上传/下载 Excel 或使用 @RequestExcel/@ResponseExcel 时调用。"
---

# Excel MVC

用于在 Spring MVC 中快速实现 Excel 导入导出，适合需要上传 Excel 解析或生成 Excel 下载的接口。

## 适用场景

- Controller 接口需要导入 Excel 并解析为 List 数据
- Controller 接口需要导出 Excel 文件（固定模型或动态列）
- 前端通过 GET/POST 请求下载 Excel（包含中文文件名）

## 核心能力

- @RequestExcel：自动解析上传文件为 List<T>
- @ResponseExcel：自动将返回值导出为 Excel 文件
- ExcelDynamicData：动态列导出，列名与中文表头由数据决定

## 使用步骤

### 1. 启用组件

```java
@SpringBootApplication
@EnableExcelMvc
public class Application {

    /**
     * 应用启动入口
     */
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 2. 固定模型导出

```java
@RestController
@RequestMapping("/report")
public class ReportController {

    /**
     * 导出质量报告
     */
    @ResponseExcel(name = "质量报告数据-{type}-{yyyyMMdd}", sheet = "报告数据")
    @GetMapping("/export")
    public List<ReportSummaryExportVO> exportExcel(@RequestParam String type) {
        return service.queryReport(type);
    }
}
```

文件名占位符(占位符非必填)：

- {yyyyMMdd}：日期格式
- {paramName}：请求参数（GET/Form）

### 3. Excel 导入

```java
@RestController
@RequestMapping("/import")
public class ImportController {

    /**
     * 导入数据
     */
    @PostMapping("/excel")
    public String importExcel(@RequestExcel List<ImportRowVO> rows) {
        service.save(rows);
        return "OK";
    }
}
```

可选配置：

- fileName：上传字段名，默认 file
- matchFilePattern：原始文件名正则校验
- throwErrorData：校验失败时是否返回错误数据

### 4. 动态列导出

```java
@RestController
@RequestMapping("/dynamic")
public class DynamicController {

    /**
     * 动态导出
     */
    @ResponseExcel(name = "动态导出", sheet = "数据")
    @PostMapping("/export")
    public ExcelDynamicData exportDynamic(@RequestBody ExportQuery query) {
        ExcelDynamicData data = new ExcelDynamicData();
        data.setColumns(Arrays.asList("name", "age", "dept"));
        data.setColumnCn(Arrays.asList("姓名", "年龄", "部门"));
        data.setRows(service.queryRows(query));
        data.setFileName("质量检查异常数据下载");
        return data;
    }
}
```

规则：

- columnCn 有值则作为表头，否则使用 columns
- rows 为 List<Map<String, Object>>，按 columns 顺序取值
- POST/JSON 场景下如需动态文件名，设置 ExcelDynamicData.fileName

## 前端下载（GET/POST）

后端已设置 Content-Disposition，并通过 Access-Control-Expose-Headers 暴露该 Header。

```javascript
axios
  .post("/api/quality/datafile/download", payload, { responseType: "blob" })
  .then((response) => {
    const disposition = response.headers["content-disposition"] || "";
    const match = disposition.match(/filename\*?=([^;]+)/i);
    const rawName = match ? match[1].replace(/['"]/g, "") : "download.xlsx";
    const fileName = decodeURIComponent(rawName.replace("utf-8''", ""));

    const blob = new Blob([response.data]);
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = fileName;
    link.click();
    window.URL.revokeObjectURL(link.href);
  });
```

## 相关引用

- 参考文件清单：[references/README.md](./references/README.md)
