import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const [, , payloadPath, outputPath] = process.argv;
if (!payloadPath || !outputPath) {
  throw new Error("Usage: node export_workbook.mjs <payload.json> <output.xlsx>");
}

const payload = JSON.parse(await fs.readFile(payloadPath, "utf8"));
const workbook = Workbook.create();
const indicatorNames = payload.method.indicator_names ?? ["rainfall", "sea_level", "flood_depth"];
const indicatorSymbols = indicatorNames.map((name, index) => {
  if (name === "rainfall") return "R";
  if (name === "sea_level") return "W";
  if (name === "storm_surge") return "S";
  if (name === "flood_depth") return "F";
  return `I${index + 1}`;
});
const severityFormula = indicatorSymbols.map(symbol => `w_${symbol} z_${symbol},t`).join(" + ");

const readme = workbook.worksheets.add("README");
readme.showGridLines = false;
readme.getRange("A1:F1").merge();
readme.getRange("A1").values = [[payload.method.title]];
readme.getRange("A1:F1").format = {
  fill: "#14324A",
  font: { bold: true, color: "#FFFFFF", size: 16 },
  verticalAlignment: "center",
};
readme.getRange("A1:F1").format.rowHeight = 30;
readme.getRange("A3:B9").values = [
  ["Method", payload.method.description],
  ["Indicators", indicatorNames.join(", ")],
  ["Severity", `H_t = ${severityFormula}`],
  ["Threshold tau_1", payload.method.tau_1],
  ["Threshold tau_2", payload.method.tau_2],
  ["Source data", payload.method.source_data],
  ["Source config", payload.method.source_config],
];
readme.getRange("A3:A9").format = { fill: "#DCEAF2", font: { bold: true, color: "#14324A" } };
readme.getRange("B6:B7").format.numberFormat = "0.000000";
readme.getRange("A3:B9").format.borders = { preset: "outside", style: "thin", color: "#AFC4D2" };
readme.getRange("A3:B9").format.wrapText = true;
readme.getRange("A:A").format.columnWidth = 24;
readme.getRange("B:B").format.columnWidth = 72;

const tableNames = {
  "Raw Input": "RawInputTable",
  "Event Results": "EventResultsTable",
  "Scenario Summary": "ScenarioSummaryTable",
  "Indicator Diagnostics": "IndicatorDiagnosticsTable",
  "Model Parameters": "ModelParametersTable",
  "Cleaning Log": "CleaningLogTable",
};

for (const [sheetName, data] of Object.entries(payload.sheets)) {
  const sheet = workbook.worksheets.add(sheetName);
  sheet.showGridLines = false;
  const matrix = [data.columns, ...data.rows];
  if (matrix.length === 0 || data.columns.length === 0) continue;
  const range = sheet.getRangeByIndexes(0, 0, matrix.length, data.columns.length);
  range.values = matrix;
  const header = sheet.getRangeByIndexes(0, 0, 1, data.columns.length);
  header.format = {
    fill: "#1F5A78",
    font: { bold: true, color: "#FFFFFF" },
    verticalAlignment: "center",
    wrapText: true,
  };
  header.format.rowHeight = 30;
  sheet.freezePanes.freezeRows(1);
  const table = sheet.tables.add(range, true, tableNames[sheetName]);
  table.style = "TableStyleMedium2";
  table.showBandedRows = true;
  table.showFilterButton = true;
  range.format.autofitColumns();
  range.format.autofitRows();
  for (let col = 0; col < data.columns.length; col += 1) {
    const columnRange = sheet.getRangeByIndexes(0, col, matrix.length, 1);
    const name = data.columns[col].toLowerCase();
    if (name.includes("probability") || name === "weight") {
      if (matrix.length > 1) sheet.getRangeByIndexes(1, col, matrix.length - 1, 1).format.numberFormat = "0.0000%";
    } else if (
      name.startsWith("z_") || name === "h_t" || name.includes("center") ||
      name.includes("bound") || name.includes("minimum") || name.includes("maximum") ||
      name.includes("std") || name.includes("conflict") || name.includes("information") ||
      name.startsWith("corr_") || name.startsWith("representative_")
    ) {
      if (matrix.length > 1) sheet.getRangeByIndexes(1, col, matrix.length - 1, 1).format.numberFormat = "0.000000";
    }
    const currentWidth = columnRange.format.columnWidth;
    if (currentWidth > 34) columnRange.format.columnWidth = 34;
    if (currentWidth < 11) columnRange.format.columnWidth = 11;
  }
}

const summary = workbook.worksheets.getItem("Scenario Summary");
const summaryRows = payload.sheets["Scenario Summary"].rows.length;
if (summaryRows > 0) {
  const probabilityIndex = payload.sheets["Scenario Summary"].columns.indexOf("probability");
  if (probabilityIndex >= 0) {
    summary.getRangeByIndexes(1, probabilityIndex, summaryRows, 1).conditionalFormats.add("dataBar", {
      color: "#2C7A7B",
      gradient: true,
    });
  }
}

const inspect = await workbook.inspect({
  kind: "table",
  range: "Scenario Summary!A1:J10",
  include: "values,formulas",
  tableMaxRows: 10,
  tableMaxCols: 12,
  maxChars: 4000,
});
console.log(inspect.ndjson);
const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
