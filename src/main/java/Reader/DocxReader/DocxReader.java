package Reader.DocxReader;

import Reader.DocxReader.Rule.Interface.ReadRule;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class DocxReader {
    public ReadRule rule;
    public DocxReader(ReadRule r){
        this.rule = r;
    }

    /**
     * 根据路径读docx文档
     * @param filePath 本地文件路径
     * @return 段落的列表（每个段落是一个字符串）
     */
    public synchronized List<String> readDoc(String filePath){
        ArrayList<String> res = new ArrayList<>();
        try (FileInputStream fis = new FileInputStream(filePath)) {
            XWPFDocument document = new XWPFDocument(fis);

            Iterator<XWPFParagraph> iterator = document.getParagraphsIterator();
            while (iterator.hasNext()) {
                XWPFParagraph paragraph = iterator.next();
                rule.addParagraph(paragraph,res);
            }

            document.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return res;
    }
}
