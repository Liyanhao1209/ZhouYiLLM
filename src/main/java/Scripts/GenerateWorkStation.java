package Scripts;

import com.sun.org.slf4j.internal.Logger;
import com.sun.org.slf4j.internal.LoggerFactory;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class GenerateWorkStation {
    private static final Logger logger = LoggerFactory.getLogger(GenerateWorkStation.class);
    public static void main(String[] args) {
        String root = args[0];

        File f = new File(root);
        assert f.isDirectory();

        dfs(f);
    }

    private static void dfs(File f) {
        StringBuilder sb = new StringBuilder();

        File[] files = f.listFiles();
        assert files != null;
        for (File child : files) {
            if(child.isDirectory()){
                dfs(child);
            }
            sb.append(child.getName()).append("\n");
        }

        File file = new File(f.getAbsolutePath()+"\\Workstation.txt");
        try{
            if(!file.exists()){
                boolean created = file.createNewFile();
                assert created;
            }
            try(FileWriter fw = new FileWriter(file)){
                fw.append(sb.toString());
            }
            System.out.println("成功为"+f.getName()+"创建工作目录");
        }catch (IOException e){
            logger.error(e.toString());
        }
    }
}
