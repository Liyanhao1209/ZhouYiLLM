package Writer.XlsWriter;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.*;

public class XlsWriter {
    public XlsWriter(){

    }

    public void writeXls(Map<String, List<String>> cols,String targetPath,String sheetName){
        try (Workbook workbook = new XSSFWorkbook();
             FileOutputStream outputStream = new FileOutputStream(targetPath)) {

            Sheet sheet = workbook.createSheet(sheetName);

            // 创建表头
            Row headerRow = sheet.createRow(0);
            Set<String> keys = cols.keySet();
            List<Iterator<String>> iterators = new ArrayList<>();
            int i = 0;
            for (String key : keys) {
                Cell headerCell = headerRow.createCell(i++);
                headerCell.setCellValue(key);
                iterators.add(cols.get(key).iterator());
            }

            // 填充数据
            i = 1;
            int j;
            boolean flag;
            do {
                flag = false;
                j = 0;
                Row row = sheet.createRow(i++);
                for (Iterator<String> iterator : iterators) {
                    if (iterator.hasNext()){
                        flag = true;
                        Cell cell = row.createCell(j);
                        cell.setCellValue(iterator.next());
                    }
                    j++;
                }
            }while(flag);

            // 写入文件
            workbook.write(outputStream);
            System.out.println("Excel文件已创建成功！");
        } catch (IOException e) {
            e.printStackTrace();

        }
    }
}
