package ${gateway_pkg};

import com.yss.cloud.dto.query.PageQuery;
import com.yss.cloud.dto.result.PageResult;
import ${model_pkg}.${domain_name};

import java.util.Optional;

public interface ${domain_name}Gateway {

    ${pk_java_type} ${method_add}(${domain_name} entity);

    boolean ${method_update}(${domain_name} entity);

    boolean ${method_delete}(${pk_java_type} ${pk_field_name});

    Optional<${domain_name}> ${method_get}(${pk_java_type} ${pk_field_name});

    PageResult<${domain_name}> ${method_page}(PageQuery query);
}
