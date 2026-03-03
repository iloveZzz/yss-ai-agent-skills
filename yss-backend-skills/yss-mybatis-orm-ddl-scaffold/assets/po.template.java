package ${base_package}.repository.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import lombok.EqualsAndHashCode;
${extra_imports}

@Data
@EqualsAndHashCode(callSuper = true)
@TableName("${table_name}")
public class ${domain_name}PO extends AuditableEntity {

${fields_block}
}
