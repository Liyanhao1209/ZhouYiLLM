package Scripts;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

class TargetDocRule{
    public String docSuffix;

    public TargetDocRule(String suffix){
        this.docSuffix = suffix;
    }

    public boolean isTargetFile(String filename){
        return filename.endsWith(docSuffix);
    }
}

public class GenerateWorkStation {
    static TargetDocRule target;
    public static void main(String[] args) throws IOException {
        String root = args[0];

        File f = new File(root);
        assert f.isDirectory();

        target = new TargetDocRule(args[1]);

        dfs(f);
    }

    private static void dfs(File f) throws IOException {
        StringBuilder sb = new StringBuilder();

        File[] files = f.listFiles();
        assert files != null;
        for (File child : files) {
            String name = child.getName();
            if(child.isDirectory()){
                dfs(child);
                sb.append(name).append("\n");
            }
            if(target.isTargetFile(name)){
                sb.append(name).append("\n");
            }
        }

        File file = new File(f.getAbsolutePath()+"\\Workstation.txt");
        if(!file.exists()){
            boolean created = file.createNewFile();
            assert created;
        }
        try(FileWriter fw = new FileWriter(file)){
            fw.append(sb.toString());
        }
        System.out.println("成功为"+f.getName()+"创建工作目录");
    }
}
