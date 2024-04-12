package Reader.DocxReader.Rule.Interface;

import org.apache.poi.xwpf.usermodel.XWPFParagraph;

import java.util.List;

public interface ReadRule {
    // 根据具体需要，决定当前段落的处理方式
    void addParagraph(XWPFParagraph paragraph, List<String> res);
}
