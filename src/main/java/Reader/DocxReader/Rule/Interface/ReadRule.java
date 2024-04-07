package Reader.DocxReader.Rule.Interface;

import org.apache.poi.xwpf.usermodel.XWPFParagraph;

import java.util.List;

public interface ReadRule {
    void addParagraph(XWPFParagraph paragraph, List<String> res);
}
